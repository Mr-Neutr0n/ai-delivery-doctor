from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import __version__
from .checks import run_checks
from .config import load_config
from .model import evidence_bundle, first_blocker
from .report import render_markdown, render_terminal


SAMPLE_CONFIG = {
    "schema": "aidoc-v1",
    "name": "local-ai-service",
    "checks": [
        {
            "id": "python-runtime",
            "stage": "environment",
            "type": "executable",
            "name": "python",
            "required": True,
        },
        {
            "id": "project-file",
            "stage": "environment",
            "type": "file",
            "path": "pyproject.toml",
            "required": True,
        },
        {
            "id": "optional-provider-key",
            "stage": "model",
            "type": "env",
            "name": "OPENAI_API_KEY",
            "required": False,
        },
    ],
}


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aidoc",
        description="Evidence-first acceptance checks for AI delivery.",
    )
    parser.add_argument("--version", action="version", version=__version__)

    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Write a starter delivery contract.")
    init.add_argument("--output", type=Path, default=Path("aidoc.json"))

    validate = sub.add_parser(
        "validate",
        help="Validate a delivery contract without running checks.",
    )
    validate.add_argument("--config", type=Path, required=True)

    doctor = sub.add_parser("doctor", help="Run delivery checks.")
    doctor.add_argument("--config", type=Path, required=True)
    doctor.add_argument("--json", type=Path, dest="json_output")
    doctor.add_argument("--markdown", type=Path, dest="markdown_output")
    doctor.add_argument(
        "--shareable",
        action="store_true",
        help=(
            "Minimize operator-supplied details in output/evidence before "
            "sharing outside the deployment environment."
        ),
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "init":
        if args.output.exists():
            raise SystemExit(
                f"refusing to overwrite existing file: {args.output}"
            )
        _write_json(args.output, SAMPLE_CONFIG)
        print(args.output)
        return 0

    try:
        config = load_config(args.config)
    except ValueError as exc:
        raise SystemExit(f"error: {exc}") from exc

    if args.command == "validate":
        print(
            f"VALID  {args.config}  "
            f"name={config.name!r} checks={len(config.checks)}"
        )
        return 0

    try:
        results = run_checks(config, shareable=args.shareable)
    except ValueError as exc:
        raise SystemExit(f"error: {exc}") from exc

    print(render_terminal(config.name, results))

    bundle = evidence_bundle(
        config.name,
        results,
        shareable=args.shareable,
    )

    if args.json_output:
        _write_json(args.json_output, bundle)

    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(
            render_markdown(config.name, results),
            encoding="utf-8",
        )

    return 1 if first_blocker(results) is not None else 0


if __name__ == "__main__":
    raise SystemExit(main())
