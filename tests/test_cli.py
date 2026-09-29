import json
import tempfile
import unittest
from pathlib import Path

from aidoc.cli import main


class CliTests(unittest.TestCase):
    def test_init_and_validate(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "aidoc.json"

            self.assertEqual(
                main(["init", "--output", str(path)]),
                0,
            )
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema"], "aidoc-v1")

            self.assertEqual(
                main(["validate", "--config", str(path)]),
                0,
            )

    def test_doctor_returns_one_on_required_blocker(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "aidoc.json"
            path.write_text(
                json.dumps(
                    {
                        "schema": "aidoc-v1",
                        "name": "broken",
                        "checks": [
                            {
                                "id": "missing",
                                "stage": "acceptance",
                                "type": "file",
                                "path": "missing.txt",
                                "required": True,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            self.assertEqual(
                main(["doctor", "--config", str(path)]),
                1,
            )


if __name__ == "__main__":
    unittest.main()
