from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Iterable

from . import __version__


VALID_STATUSES = {"PASS", "WARN", "FAIL"}


@dataclass(frozen=True)
class CheckSpec:
    check_id: str
    stage: str
    check_type: str
    required: bool
    options: dict


@dataclass(frozen=True)
class CheckResult:
    check_id: str
    stage: str
    check_type: str
    required: bool
    status: str
    detail: str

    def __post_init__(self) -> None:
        if self.status not in VALID_STATUSES:
            raise ValueError(f"invalid status: {self.status}")


def first_blocker(results: Iterable[CheckResult]) -> CheckResult | None:
    for result in results:
        if result.required and result.status == "FAIL":
            return result
    return None


def result_counts(results: Iterable[CheckResult]) -> dict[str, int]:
    counts = {status: 0 for status in ("PASS", "WARN", "FAIL")}
    for result in results:
        counts[result.status] += 1
    return counts


def evidence_bundle(
    name: str,
    results: list[CheckResult],
    *,
    shareable: bool = False,
) -> dict:
    blocker = first_blocker(results)
    return {
        "schema": "aidoc-evidence-v1",
        "toolVersion": __version__,
        "name": name,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "shareable": shareable,
        "summary": result_counts(results),
        "firstBlockingCheck": blocker.check_id if blocker else None,
        "checks": [asdict(result) for result in results],
    }
