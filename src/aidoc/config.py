from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .model import CheckSpec


SUPPORTED_TYPES = {"file", "env", "executable", "tcp", "http"}


@dataclass(frozen=True)
class DeliveryConfig:
    name: str
    base_dir: Path
    checks: tuple[CheckSpec, ...]


def _require_string(data: dict, key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    return value.strip()


def load_config(path: Path) -> DeliveryConfig:
    path = path.expanduser().resolve()

    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"cannot read config: {exc}") from exc

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"config must contain valid JSON: {exc.msg}") from exc

    if not isinstance(data, dict):
        raise ValueError("config root must be a JSON object")
    if data.get("schema") != "aidoc-v1":
        raise ValueError("schema must be 'aidoc-v1'")

    name = _require_string(data, "name")
    raw_checks = data.get("checks")
    if not isinstance(raw_checks, list) or not raw_checks:
        raise ValueError("checks must be a non-empty JSON array")

    seen: set[str] = set()
    checks: list[CheckSpec] = []

    for index, item in enumerate(raw_checks, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"check #{index} must be a JSON object")

        check_id = _require_string(item, "id")
        if check_id in seen:
            raise ValueError(f"duplicate check id: {check_id}")
        seen.add(check_id)

        stage = _require_string(item, "stage")
        check_type = _require_string(item, "type")
        if check_type not in SUPPORTED_TYPES:
            expected = ", ".join(sorted(SUPPORTED_TYPES))
            raise ValueError(
                f"unsupported check type {check_type!r}; expected one of {expected}"
            )

        required = item.get("required", True)
        if not isinstance(required, bool):
            raise ValueError(f"{check_id}.required must be true or false")

        options = {
            key: value
            for key, value in item.items()
            if key not in {"id", "stage", "type", "required"}
        }

        checks.append(
            CheckSpec(
                check_id=check_id,
                stage=stage,
                check_type=check_type,
                required=required,
                options=options,
            )
        )

    return DeliveryConfig(
        name=name,
        base_dir=path.parent,
        checks=tuple(checks),
    )
