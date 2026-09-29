import json
import os
import unittest
from unittest.mock import patch

from aidoc.checks import check_openai_compatible
from aidoc.model import CheckSpec


class _Response:
    def __init__(self, payload: dict, status: int = 200):
        self.status = status
        self._raw = json.dumps(payload).encode("utf-8")

    def read(self):
        return self._raw

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class OpenAICompatibleTests(unittest.TestCase):
    def test_catalog_check_passes_without_sdk(self):
        spec = CheckSpec(
            "local-models",
            "model",
            "openai-compatible",
            True,
            {"base_url": "http://127.0.0.1:11434/v1"},
        )

        with patch(
            "urllib.request.urlopen",
            return_value=_Response(
                {"data": [{"id": "qwen3:8b"}, {"id": "llama3.2"}]}
            ),
        ) as urlopen:
            result = check_openai_compatible(spec)

        self.assertEqual(result.status, "PASS")
        self.assertIn("2 models", result.detail)

        request = urlopen.call_args.args[0]
        self.assertEqual(
            request.full_url,
            "http://127.0.0.1:11434/v1/models",
        )

    def test_requested_model_must_exist(self):
        spec = CheckSpec(
            "required-model",
            "model",
            "openai-compatible",
            True,
            {
                "base_url": "https://example.test/v1",
                "model": "required-model",
            },
        )

        with patch(
            "urllib.request.urlopen",
            return_value=_Response({"data": [{"id": "other-model"}]}),
        ):
            result = check_openai_compatible(spec)

        self.assertEqual(result.status, "FAIL")
        self.assertIn("required-model", result.detail)

    def test_api_key_is_read_from_env_but_not_logged(self):
        spec = CheckSpec(
            "provider",
            "model",
            "openai-compatible",
            True,
            {
                "base_url": "https://api.example.test/v1",
                "api_key_env": "AIDOC_PROVIDER_KEY",
            },
        )

        with patch.dict(
            os.environ,
            {"AIDOC_PROVIDER_KEY": "very-secret-value"},
        ):
            with patch(
                "urllib.request.urlopen",
                return_value=_Response({"data": [{"id": "model"}]}),
            ) as urlopen:
                result = check_openai_compatible(spec)

        self.assertEqual(result.status, "PASS")
        self.assertNotIn("very-secret-value", result.detail)
        request = urlopen.call_args.args[0]
        self.assertEqual(
            request.headers["Authorization"],
            "Bearer very-secret-value",
        )

    def test_missing_required_key_fails_without_network(self):
        spec = CheckSpec(
            "provider",
            "model",
            "openai-compatible",
            True,
            {
                "base_url": "https://api.example.test/v1",
                "api_key_env": "AIDOC_MISSING_KEY",
            },
        )

        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("AIDOC_MISSING_KEY", None)
            with patch("urllib.request.urlopen") as urlopen:
                result = check_openai_compatible(spec)

        self.assertEqual(result.status, "FAIL")
        urlopen.assert_not_called()


if __name__ == "__main__":
    unittest.main()
