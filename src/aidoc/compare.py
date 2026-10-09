from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .model import CheckResult


STATUS_RANK = {"PASS": 0, "WARN": 1, "FAIL": 2}


@dataclass(frozen=True)
class EvidenceCheck:
    check_id: str
    stage: str
    check_type: str
    required: bool
    status: str
    detail: str


@dataclass(frozen=True)
class EvidenceChange:
    check_id: str
    stage: str
    required: bool
    before: str | None
    after: str | None
    change: str


def _read_evidence_document(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"cannot read evidence: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"evidence must contain valid JSON: {exc.msg}") from exc

    if not isinstance(data, dict) or data.get("schema") != "aidoc-evidence-v1":
        raise ValueError("evidence schema must be 'aidoc-evidence-v1'")

    return data


def _parse_raw_checks(raw_checks: object) -> list[EvidenceCheck]:
    if not isinstance(raw_checks, list):
        raise ValueError("evidence checks must be an array")

    checks: list[EvidenceCheck] = []
    seen: set[str] = set()

    for index, item in enumerate(raw_checks, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"evidence check #{index} must be an object")

        check_id = item.get("check_id")
        stage = item.get("stage")
        check_type = item.get("check_type")
        required = item.get("required")
        status = item.get("status")
        detail = item.get("detail")

        if not isinstance(check_id, str) or not check_id:
            raise ValueError(f"evidence check #{index} has invalid check_id")
        if check_id in seen:
            raise ValueError(f"duplicate evidence check id: {check_id}")
        if not isinstance(stage, str) or not stage:
            raise ValueError(f"{check_id}.stage must be a non-empty string")
        if not isinstance(check_type, str) or not check_type:
            raise ValueError(f"{check_id}.check_type must be a non-empty string")
        if not isinstance(required, bool):
            raise ValueError(f"{check_id}.required must be boolean")
        if status not in STATUS_RANK:
            raise ValueError(f"{check_id}.status is invalid")
        if not isinstance(detail, str):
            raise ValueError(f"{check_id}.detail must be a string")

        seen.add(check_id)
        checks.append(
            EvidenceCheck(
                check_id=check_id,
                stage=stage,
                check_type=check_type,
                required=required,
                status=status,
                detail=detail,
            )
        )

    return checks


def _load_checks(path: Path) -> dict[str, EvidenceCheck]:
    data = _read_evidence_document(path)
    return {check.check_id: check for check in _parse_raw_checks(data.get("checks"))}


def load_evidence_results(path: Path) -> tuple[str, list[CheckResult], bool]:
    data = _read_evidence_document(path)
    name = data.get("name")
    if not isinstance(name, str) or not name:
        raise ValueError("evidence name must be a non-empty string")

    results = [
        CheckResult(
            check.check_id,
            check.stage,
            check.check_type,
            check.required,
            check.status,
            check.detail,
        )
        for check in _parse_raw_checks(data.get("checks"))
    ]
    # Fail safe: a missing or malformed flag reads as not shareable so the report
    # warns instead of assuming the bundle is safe to disclose.
    return name, results, data.get("shareable") is True


def compare_evidence(before_path: Path, after_path: Path) -> list[EvidenceChange]:
    before = _load_checks(before_path)
    after = _load_checks(after_path)

    ordered_ids = list(before)
    ordered_ids.extend(check_id for check_id in after if check_id not in before)

    changes: list[EvidenceChange] = []

    for check_id in ordered_ids:
        old = before.get(check_id)
        new = after.get(check_id)

        if old is None and new is not None:
            changes.append(
                EvidenceChange(
                    check_id,
                    new.stage,
                    new.required,
                    None,
                    new.status,
                    "ADDED",
                )
            )
            continue

        if new is None and old is not None:
            changes.append(
                EvidenceChange(
                    check_id,
                    old.stage,
                    old.required,
                    old.status,
                    None,
                    "REMOVED",
                )
            )
            continue

        assert old is not None and new is not None

        if old.status == new.status:
            change = "UNCHANGED"
        elif STATUS_RANK[new.status] < STATUS_RANK[old.status]:
            change = "IMPROVED"
        else:
            change = "REGRESSED"

        changes.append(
            EvidenceChange(
                check_id,
                new.stage,
                new.required,
                old.status,
                new.status,
                change,
            )
        )

    return changes


def has_required_regression(changes: list[EvidenceChange]) -> bool:
    return any(
        change.required and change.change == "REGRESSED"
        for change in changes
    )


def render_terminal(changes: list[EvidenceChange]) -> str:
    if not changes:
        return "No checks found."

    width = max(len(change.check_id) for change in changes)
    lines = ["AI Delivery Doctor - evidence comparison", ""]

    for change in changes:
        before = change.before or "-"
        after = change.after or "-"
        lines.append(
            f"{change.change:9}  {change.check_id:<{width}}  "
            f"{before:4} -> {after:4}  "
            f"[{change.stage}/"
            f"{'required' if change.required else 'optional'}]"
        )

    return "\n".join(lines)


def render_markdown(changes: list[EvidenceChange]) -> str:
    counts: dict[str, int] = {}
    for change in changes:
        counts[change.change] = counts.get(change.change, 0) + 1

    lines = [
        "# AI Delivery Doctor Evidence Comparison",
        "",
        (
            "**Summary:** "
            + " · ".join(
                f"{count} {name}"
                for name, count in sorted(counts.items())
            )
        ),
        "",
        "| Change | Check | Before | After | Stage | Required |",
        "|---|---|---:|---:|---|---|",
    ]

    for change in changes:
        lines.append(
            f"| {change.change} | `{change.check_id}` | "
            f"{change.before or '-'} | {change.after or '-'} | "
            f"{change.stage} | {'yes' if change.required else 'no'} |"
        )

    lines.extend(
        [
            "",
            "> A status change is evidence about the bounded check only. "
            "It is not, by itself, proof of the ultimate root cause.",
            "",
        ]
    )

    return "\n".join(lines)
