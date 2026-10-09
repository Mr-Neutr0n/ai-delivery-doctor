import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from aidoc.checks import (
    _safe_url_label,
    check_directory,
    check_env,
    check_file,
    run_check,
    sanitize_result,
)
from aidoc.config import load_config
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

    def test_directory_check_pass_fail_warn_and_not_a_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "models").mkdir()
            (root / "not-a-dir.txt").write_text("x", encoding="utf-8")

            good = CheckSpec(
                "dir-ok",
                "environment",
                "directory",
                True,
                {"path": "models"},
            )
            missing_required = CheckSpec(
                "dir-missing",
                "environment",
                "directory",
                True,
                {"path": "missing"},
            )
            missing_optional = CheckSpec(
                "dir-optional",
                "environment",
                "directory",
                False,
                {"path": "optional-missing"},
            )
            file_not_dir = CheckSpec(
                "dir-file",
                "environment",
                "directory",
                True,
                {"path": "not-a-dir.txt"},
            )

            self.assertEqual(check_directory(good, root).status, "PASS")
            self.assertEqual(check_directory(missing_required, root).status, "FAIL")
            self.assertEqual(check_directory(missing_optional, root).status, "WARN")
            self.assertEqual(check_directory(file_not_dir, root).status, "FAIL")

    def test_directory_check_resolves_a_relative_path_from_the_loaded_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "models").mkdir()
            contract = root / "aidoc.json"
            contract.write_text(
                json.dumps(
                    {
                        "schema": "aidoc-v1",
                        "name": "directory-route",
                        "checks": [
                            {
                                "id": "model-cache-dir",
                                "stage": "environment",
                                "type": "directory",
                                "path": "models",
                                "required": True,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            config = load_config(contract)

            self.assertEqual(config.base_dir, root.resolve())
            self.assertEqual(run_check(config.checks[0], config).status, "PASS")

    @unittest.skipIf(os.name == "nt", "POSIX directory permissions")
    def test_directory_check_turns_an_unreadable_path_into_a_bounded_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            blocked = root / "blocked"
            blocked.mkdir()
            (blocked / "models").mkdir()
            blocked.chmod(0o000)
            try:
                spec = CheckSpec(
                    "blocked-dir",
                    "environment",
                    "directory",
                    True,
                    {"path": "blocked/models"},
                )
                result = check_directory(spec, root)
            finally:
                blocked.chmod(0o755)

            # Older Pythons raise from exists(); 3.14 answers False. Either way the
            # probe stays a bounded FAIL and never leaks the absolute path.
            self.assertEqual(result.status, "FAIL")
            self.assertTrue(
                "PermissionError" in result.detail
                or "required path not found" in result.detail,
                result.detail,
            )
            self.assertNotIn(str(root), result.detail)

    def test_directory_check_turns_an_oserror_into_a_bounded_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = CheckSpec(
                "blocked-dir",
                "environment",
                "directory",
                True,
                {"path": "blocked"},
            )
            with patch.object(
                Path, "exists", side_effect=PermissionError(13, "Permission denied")
            ):
                result = check_directory(spec, Path(tmp))

            self.assertEqual(result.status, "FAIL")
            self.assertEqual(
                result.detail, "PermissionError: unable to inspect directory: blocked"
            )

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

    def test_shareable_result_minimizes_directory_detail(self):
        result = CheckResult(
            "model-cache-dir",
            "environment",
            "directory",
            True,
            "FAIL",
            "/private/customer/site/models was not found",
        )
        safe = sanitize_result(result)

        self.assertNotIn("customer", safe.detail)
        self.assertNotIn("/private/", safe.detail)
        self.assertNotIn("models", safe.detail)
        self.assertEqual(safe.status, "FAIL")


if __name__ == "__main__":
    unittest.main()
