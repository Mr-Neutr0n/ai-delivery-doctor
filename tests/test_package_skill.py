import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.package_skill import build_skill_archive


class PackageSkillTests(unittest.TestCase):
    def test_builds_deterministic_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "demo-skill"
            (skill / "references").mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: demo-skill\ndescription: Demo.\n---\n",
                encoding="utf-8",
            )
            (skill / "references" / "guide.md").write_text(
                "# Guide\n",
                encoding="utf-8",
            )

            first = root / "first.zip"
            second = root / "second.zip"

            build_skill_archive(skill, first)
            build_skill_archive(skill, second)

            self.assertEqual(first.read_bytes(), second.read_bytes())

            with zipfile.ZipFile(first) as archive:
                self.assertEqual(
                    archive.namelist(),
                    [
                        "demo-skill/SKILL.md",
                        "demo-skill/references/guide.md",
                    ],
                )


if __name__ == "__main__":
    unittest.main()
