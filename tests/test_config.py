import json
import tempfile
import unittest
from pathlib import Path

from aidoc.config import load_config


class ConfigTests(unittest.TestCase):
    def test_loads_ordered_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "aidoc.json"
            path.write_text(
                json.dumps(
                    {
                        "schema": "aidoc-v1",
                        "name": "demo",
                        "checks": [
                            {
                                "id": "python",
                                "stage": "environment",
                                "type": "executable",
                                "name": "python",
                                "required": True,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            config = load_config(path)

            self.assertEqual(config.name, "demo")
            self.assertEqual(config.checks[0].check_id, "python")

    def test_rejects_duplicate_check_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "aidoc.json"
            item = {
                "id": "same",
                "stage": "environment",
                "type": "file",
                "path": "x",
            }
            path.write_text(
                json.dumps(
                    {
                        "schema": "aidoc-v1",
                        "name": "demo",
                        "checks": [item, item],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "duplicate"):
                load_config(path)

    def test_rejects_unknown_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "aidoc.json"
            path.write_text(
                '{"schema":"other","name":"demo","checks":[]}',
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "aidoc-v1"):
                load_config(path)


if __name__ == "__main__":
    unittest.main()
