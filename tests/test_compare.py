import json
import tempfile
import unittest
from pathlib import Path

from aidoc.compare import (
    compare_evidence,
    has_required_regression,
    render_markdown,
)
from aidoc.model import CheckResult, evidence_bundle


def _write(path: Path, checks: list[dict]) -> None:
    path.write_text(
        json.dumps(
            {
                "schema": "aidoc-evidence-v1",
                "name": "demo",
                "generatedAt": "2026-01-01T00:00:00Z",
                "shareable": False,
                "summary": {},
                "firstBlockingCheck": None,
                "checks": checks,
            }
        ),
        encoding="utf-8",
    )


class CompareTests(unittest.TestCase):
    def test_detects_improvement_and_required_regression(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            before = root / "before.json"
            after = root / "after.json"

            _write(
                before,
                [
                    {
                        "check_id": "model",
                        "stage": "model",
                        "check_type": "env",
                        "required": True,
                        "status": "FAIL",
                        "detail": "missing",
                    },
                    {
                        "check_id": "tool",
                        "stage": "tools",
                        "check_type": "tcp",
                        "required": True,
                        "status": "PASS",
                        "detail": "up",
                    },
                ],
            )

            _write(
                after,
                [
                    {
                        "check_id": "model",
                        "stage": "model",
                        "check_type": "env",
                        "required": True,
                        "status": "PASS",
                        "detail": "set",
                    },
                    {
                        "check_id": "tool",
                        "stage": "tools",
                        "check_type": "tcp",
                        "required": True,
                        "status": "FAIL",
                        "detail": "down",
                    },
                ],
            )

            changes = compare_evidence(before, after)
            by_id = {change.check_id: change for change in changes}

            self.assertEqual(by_id["model"].change, "IMPROVED")
            self.assertEqual(by_id["tool"].change, "REGRESSED")
            self.assertTrue(has_required_regression(changes))

            report = render_markdown(changes)
            self.assertIn("IMPROVED", report)
            self.assertIn("REGRESSED", report)

    def test_added_and_removed_are_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            before = root / "before.json"
            after = root / "after.json"

            _write(
                before,
                [
                    {
                        "check_id": "old",
                        "stage": "environment",
                        "check_type": "file",
                        "required": False,
                        "status": "PASS",
                        "detail": "ok",
                    }
                ],
            )
            _write(
                after,
                [
                    {
                        "check_id": "new",
                        "stage": "environment",
                        "check_type": "file",
                        "required": False,
                        "status": "PASS",
                        "detail": "ok",
                    }
                ],
            )

            changes = compare_evidence(before, after)
            by_id = {change.check_id: change.change for change in changes}

            self.assertEqual(by_id["old"], "REMOVED")
            self.assertEqual(by_id["new"], "ADDED")

    def test_rejects_duplicate_and_malformed_check_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            duplicate = root / "duplicate.json"
            item = {
                "check_id": "same",
                "stage": "environment",
                "check_type": "file",
                "required": True,
                "status": "PASS",
                "detail": "ok",
            }
            _write(duplicate, [item, dict(item)])

            with self.assertRaisesRegex(
                ValueError, "duplicate evidence check id: same"
            ):
                compare_evidence(duplicate, duplicate)

            malformed = root / "malformed.json"
            _write(
                malformed,
                [
                    {
                        "check_id": "model",
                        "stage": "model",
                        "required": True,
                        "status": "PASS",
                        "detail": "ok",
                    }
                ],
            )

            with self.assertRaisesRegex(ValueError, "check_type"):
                compare_evidence(malformed, malformed)

    def test_v1_evidence_written_by_doctor_compares_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "evidence.json"
            bundle = evidence_bundle(
                "demo",
                [
                    CheckResult("model", "model", "env", True, "PASS", "set"),
                    CheckResult("tool", "tools", "tcp", False, "WARN", "slow"),
                ],
            )
            path.write_text(json.dumps(bundle), encoding="utf-8")

            changes = compare_evidence(path, path)

            self.assertEqual(
                [change.change for change in changes],
                ["UNCHANGED", "UNCHANGED"],
            )


if __name__ == "__main__":
    unittest.main()
