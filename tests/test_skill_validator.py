import tempfile
import unittest
from pathlib import Path

from scripts.validate_skill import validate_skill


class SkillValidatorTests(unittest.TestCase):
    def test_repository_skill_is_valid(self):
        root = Path(__file__).resolve().parents[1]
        metadata = validate_skill(
            root / ".agents" / "skills" / "ai-delivery-doctor"
        )
        self.assertEqual(metadata.name, "ai-delivery-doctor")

    def test_name_must_match_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "demo-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "---\n"
                "name: other-skill\n"
                "description: A useful demo skill.\n"
                "---\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "must match"):
                validate_skill(skill)

    def test_missing_description_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "demo-skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "---\n"
                "name: demo-skill\n"
                "---\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "description"):
                validate_skill(skill)


if __name__ == "__main__":
    unittest.main()
