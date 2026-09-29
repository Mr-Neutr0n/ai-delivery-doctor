"""Dependency-free validation for Agent Skill packaging."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class SkillMetadata:
    name: str
    description: str


def parse_skill_metadata(skill_file: Path) -> SkillMetadata:
    try:
        text = skill_file.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"cannot read SKILL.md: {exc}") from exc

    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")

    parts = text.split("---", 2)
    if len(parts) != 3:
        raise ValueError("SKILL.md frontmatter is not closed")

    frontmatter = parts[1]

    name_match = re.search(
        r"^name:\s*([^\n]+)$",
        frontmatter,
        re.MULTILINE,
    )
    description_match = re.search(
        r"^description:\s*([^\n]+)$",
        frontmatter,
        re.MULTILINE,
    )

    if name_match is None:
        raise ValueError("SKILL.md frontmatter requires name")
    if description_match is None:
        raise ValueError("SKILL.md frontmatter requires description")

    return SkillMetadata(
        name=name_match.group(1).strip(),
        description=description_match.group(1).strip(),
    )


def validate_skill(skill_dir: Path) -> SkillMetadata:
    skill_dir = skill_dir.resolve()
    skill_file = skill_dir / "SKILL.md"

    if not skill_dir.is_dir():
        raise ValueError(f"skill directory not found: {skill_dir}")
    if not skill_file.is_file():
        raise ValueError("skill directory must contain SKILL.md")

    metadata = parse_skill_metadata(skill_file)

    if metadata.name != skill_dir.name:
        raise ValueError(
            f"skill name {metadata.name!r} must match directory "
            f"{skill_dir.name!r}"
        )
    if len(metadata.name) > 64 or not NAME_RE.fullmatch(metadata.name):
        raise ValueError(
            "skill name must be <=64 chars using lowercase letters, "
            "numbers, and single hyphens"
        )
    if not metadata.description:
        raise ValueError("skill description must not be empty")
    if len(metadata.description) > 1024:
        raise ValueError("skill description must be <=1024 characters")

    line_count = len(skill_file.read_text(encoding="utf-8").splitlines())
    if line_count > 500:
        raise ValueError(
            f"SKILL.md has {line_count} lines; keep it at or below 500 "
            "and move detail into references/"
        )

    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the repository's Agent Skill contract."
    )
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()

    try:
        metadata = validate_skill(args.skill_dir)
    except ValueError as exc:
        raise SystemExit(f"INVALID: {exc}") from exc

    print(
        f"VALID  {args.skill_dir}  "
        f"name={metadata.name!r} "
        f"description_chars={len(metadata.description)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
