import unittest

from aidoc import __version__
from aidoc.model import CheckResult, evidence_bundle


class EvidenceContractTests(unittest.TestCase):
    def test_evidence_records_tool_version_and_stable_core_fields(self):
        bundle = evidence_bundle(
            "demo",
            [
                CheckResult(
                    "runtime",
                    "environment",
                    "executable",
                    True,
                    "PASS",
                    "available",
                )
            ],
        )

        self.assertEqual(bundle["schema"], "aidoc-evidence-v1")
        self.assertEqual(bundle["toolVersion"], __version__)
        self.assertEqual(
            set(bundle["summary"]),
            {"PASS", "WARN", "FAIL"},
        )
        self.assertIsNone(bundle["firstBlockingCheck"])
        self.assertEqual(bundle["checks"][0]["check_id"], "runtime")

    def test_first_blocker_is_recorded(self):
        bundle = evidence_bundle(
            "demo",
            [
                CheckResult(
                    "provider",
                    "model",
                    "env",
                    True,
                    "FAIL",
                    "missing",
                )
            ],
        )

        self.assertEqual(bundle["firstBlockingCheck"], "provider")
        self.assertEqual(bundle["summary"]["FAIL"], 1)


if __name__ == "__main__":
    unittest.main()
