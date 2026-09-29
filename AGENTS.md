# AGENTS.md

This is the working contract for coding agents contributing to AI Delivery Doctor.

## Mission

Build a local-first, evidence-driven acceptance tool for AI application delivery.

## Non-negotiable rules

- Never log secret values.
- Never execute arbitrary shell commands from a delivery contract.
- Network probes must be explicit.
- Do not mutate target systems in diagnostic code.
- Do not turn a failed probe into an unsupported root-cause claim.
- Preserve check order and deterministic output where practical.
- Add regression tests for behavior changes.
- Keep the core vendor-neutral.
- Use synthetic/local fixtures in tests.

## Validate

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

## Design boundary

Model/Agent reasoning may help define **what should be verified**.

The deterministic core must remain responsible for **what was actually observed**.
