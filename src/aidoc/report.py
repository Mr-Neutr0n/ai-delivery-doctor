from __future__ import annotations

from .model import CheckResult, first_blocker, result_counts


def render_terminal(name: str, results: list[CheckResult]) -> str:
    width = max(len(result.check_id) for result in results)
    lines = [f"AI Delivery Doctor - {name}", ""]

    for result in results:
        requirement = "required" if result.required else "optional"
        lines.append(
            f"{result.status:4}  {result.check_id:<{width}}  "
            f"[{result.stage}/{requirement}]  {result.detail}"
        )

    blocker = first_blocker(results)
    lines.append("")

    if blocker is None:
        lines.append("FIRST BLOCKER  none among required checks")
    else:
        lines.append(
            f"FIRST BLOCKER  {blocker.check_id} (stage={blocker.stage})"
        )
        lines.append(
            "NOTE           This is the first unsupported required transition, "
            "not a proven root cause."
        )

    return "\n".join(lines)


def render_markdown(name: str, results: list[CheckResult]) -> str:
    counts = result_counts(results)

    lines = [
        f"# AI Delivery Doctor Report — {name}",
        "",
        (
            f"**Summary:** {counts['PASS']} PASS · "
            f"{counts['WARN']} WARN · {counts['FAIL']} FAIL"
        ),
        "",
        "## Delivery checks",
        "",
    ]

    for result in results:
        requirement = "required" if result.required else "optional"
        lines.append(
            f"- **{result.status}** `{result.check_id}` "
            f"— {result.stage} / {requirement} — {result.detail}"
        )

    blocker = first_blocker(results)
    lines.extend(["", "## First blocking transition", ""])

    if blocker is None:
        lines.append("No required check failed.")
    else:
        lines.append(
            f"`{blocker.check_id}` in stage `{blocker.stage}` is the first "
            "required check that could not be proven."
        )
        lines.append("")
        lines.append(
            "> This is a triage boundary, not a claim that the check is the "
            "ultimate root cause."
        )

    lines.extend(
        [
            "",
            "## Interpretation rule",
            "",
            "A passing upstream probe must not be generalized into a claim "
            "that the downstream user outcome works. Verify the next "
            "transition explicitly.",
            "",
        ]
    )

    return "\n".join(lines)
