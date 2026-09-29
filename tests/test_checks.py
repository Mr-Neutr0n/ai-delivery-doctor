import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from aidoc.checks import (
    _safe_url_label,
    check_env,
    check_file,
    sanitize_result,
)
from aidoc.model import CheckResult, CheckSpec


class CheckTests(unittest.TestCase):
    def test_file_check_pass_and_required_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ok.txt").write_text("ok", encoding="utf-8")

            good = CheckSpec(
                "file-ok",
                "environment",
                "file",
                True,
                {"path": "ok.txt"},
            )
            missing = CheckSpec(
                "file-missing",
                "environment",
                "file",
                True,
                {"path": "missing.txt"},
            )

            self.assertEqual(check_file(good, root).status, "PASS")
            self.assertEqual(check_file(missing, root).status, "FAIL")

    def test_optional_missing_env_is_warn_and_never_prints_value(self):
        spec = CheckSpec(
            "provider-key",
            "model",
            "env",
            False,
            {"name": "AIDOC_TEST_SECRET"},
        )

        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("AIDOC_TEST_SECRET", None)
            result = check_env(spec)
            self.assertEqual(result.status, "WARN")

        with patch.dict(
            os.environ,
            {"AIDOC_TEST_SECRET": "super-secret-value"},
        ):
            result = check_env(spec)
            self.assertEqual(result.status, "PASS")
            self.assertNotIn("super-secret-value", result.detail)

    def test_http_label_removes_credentials_query_and_fragment(self):
        label = _safe_url_label(
            "https://demo:secret@example.test:8443/health"
            "?token=secret#fragment"
        )
        self.assertEqual(label, "https://example.test:8443/health")
        self.assertNotIn("secret", label)
        self.assertNotIn("token", label)

    def test_shareable_result_minimizes_file_detail(self):
        result = CheckResult(
            "customer-config",
            "environment",
            "file",
            True,
            "FAIL",
            "/private/customer/site/config.json was not found",
        )
        safe = sanitize_result(result)

        self.assertNotIn("customer", safe.detail)
        self.assertNotIn("/private/", safe.detail)
        self.assertEqual(safe.status, "FAIL")


if __name__ == "__main__":
    unittest.main()
