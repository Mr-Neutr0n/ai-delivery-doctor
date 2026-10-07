import json
import tempfile
import unittest
from pathlib import Path

from aidoc.cli import main
from aidoc.compare import load_evidence_results


def _write_bundle(path: Path, *, name: str = "demo", checks: list[dict]) -> None:
    path.write_text(
        json.dumps(
            {
                "schema": "aidoc-evidence-v1",
                "toolVersion": "0.0.0",
                "name": name,
                "generatedAt": "2026-01-01T00:00:00Z",
                "shareable": True,
                "summary": {"PASS": 0, "WARN": 0, "FAIL": 0},
                "firstBlockingCheck": None,
                "checks": checks,
            }
        ),
        encoding="utf-8",
    )


class EvidenceReportTests(unittest.TestCase):
    def test_load_preserves_check_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "evidence.json"
            _write_bundle(
                path,
                checks=[
                    {
                        "check_id": "first",
                        "stage": "environment",
                        "check_type": "file",
                        "required": True,
                        "status": "PASS",
                        "detail": "ok",
                    },
                    {
                        "check_id": "second",
                        "stage": "model",
                        "check_type": "env",
                        "required": True,
                        "status": "FAIL",
                        "detail": "missing",
                    },
                ],
            )

            name, results = load_evidence_results(path)
            self.assertEqual(name, "demo")
            self.assertEqual([r.check_id for r in results], ["first", "second"])

    def test_report_writes_markdown_without_running_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence = root / "evidence.json"
            report_path = root / "report.md"
            _write_bundle(
                evidence,
                checks=[
                    {
                        "check_id": "blocker",
                        "stage": "acceptance",
                        "check_type": "file",
                        "required": True,
                        "status": "FAIL",
                        "detail": "missing artifact",
                    }
                ],
            )

            self.assertEqual(
                main(
                    [
                        "report",
                        str(evidence),
                        "--markdown",
                        str(report_path),
                    ]
                ),
                1,
            )

            report = report_path.read_text(encoding="utf-8")
            self.assertIn("1 FAIL", report)
            self.assertIn("`blocker`", report)

    def test_malformed_evidence_exits_with_clear_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text('{"schema": "aidoc-v2"}', encoding="utf-8")

            with self.assertRaises(SystemExit) as ctx:
                main(["report", str(path)])

            self.assertIn("aidoc-evidence-v1", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
