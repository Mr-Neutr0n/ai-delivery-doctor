"""One-command deterministic showcase for AI Delivery Doctor."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from aidoc.checks import run_checks
from aidoc.compare import compare_evidence, render_terminal as render_compare
from aidoc.config import load_config
from aidoc.model import evidence_bundle, first_blocker
from aidoc.report import render_terminal


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def run_showcase() -> int:
    """Run a synthetic before/after delivery acceptance scenario."""

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        contract_path = root / "aidoc.json"
        acceptance_artifact = root / "handoff-receipt.txt"

        _write_json(
            contract_path,
            {
                "schema": "aidoc-v1",
                "name": "synthetic-ai-handoff",
                "checks": [
                    {
                        "id": "python-runtime",
                        "stage": "environment",
                        "type": "executable",
                        "name": "python",
                        "required": True,
                    },
                    {
                        "id": "handoff-receipt",
                        "stage": "acceptance",
                        "type": "file",
                        "path": "handoff-receipt.txt",
                        "required": True,
                    },
                ],
            },
        )

        config = load_config(contract_path)

        before = run_checks(config)
        before_path = root / "before.json"
        _write_json(
            before_path,
            evidence_bundle(config.name, before),
        )

        print("=== BEFORE: delivery condition is missing ===")
        print(render_terminal(config.name, before))
        print()

        if first_blocker(before) is None:
            print("SHOWCASE ERROR: expected a blocker before repair")
            return 2

        acceptance_artifact.write_text(
            "synthetic acceptance evidence\n",
            encoding="utf-8",
        )

        after = run_checks(config)
        after_path = root / "after.json"
        _write_json(
            after_path,
            evidence_bundle(config.name, after),
        )

        print("=== AFTER: the required condition is now observable ===")
        print(render_terminal(config.name, after))
        print()

        if first_blocker(after) is not None:
            print("SHOWCASE ERROR: blocker remained after repair")
            return 3

        changes = compare_evidence(before_path, after_path)

        print("=== EVIDENCE DIFF ===")
        print(render_compare(changes))
        print()

        improved = [
            change
            for change in changes
            if change.check_id == "handoff-receipt"
            and change.change == "IMPROVED"
        ]

        if not improved:
            print("SHOWCASE ERROR: expected the acceptance check to improve")
            return 4

        print(
            "SHOWCASE PASS: the same delivery contract captured a required "
            "FAIL, a verified repair condition, and an IMPROVED evidence diff."
        )
        print(
            "No production service, credential, model API, or customer data "
            "was used."
        )
        return 0


def main() -> int:
    return run_showcase()


if __name__ == "__main__":
    raise SystemExit(main())
