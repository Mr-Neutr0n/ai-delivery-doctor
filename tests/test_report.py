import unittest

from aidoc.model import CheckResult, first_blocker
from aidoc.report import render_markdown


class ReportTests(unittest.TestCase):
    def test_first_blocker_uses_required_order(self):
        results = [
            CheckResult("a", "environment", "file", True, "PASS", "ok"),
            CheckResult("b", "model", "env", False, "WARN", "optional"),
            CheckResult("c", "tools", "tcp", True, "FAIL", "down"),
            CheckResult(
                "d",
                "operator",
                "http",
                True,
                "FAIL",
                "downstream",
            ),
        ]

        self.assertEqual(first_blocker(results).check_id, "c")

        report = render_markdown("demo", results)
        self.assertIn("2 FAIL", report)
        self.assertIn("`c`", report)
        self.assertIn("not a claim", report)


if __name__ == "__main__":
    unittest.main()
