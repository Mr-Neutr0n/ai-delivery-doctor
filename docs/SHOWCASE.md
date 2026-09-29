# 3-Minute Reproducible Showcase

This is the shortest path for a reviewer or new user to understand AI Delivery Doctor.

## Minute 1 — prove the project runs

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
aidoc doctor --config examples/acceptance.example.json
```

Expected idea:

```text
PASS  required runtime/file checks
WARN  optional provider key may be absent
FIRST BLOCKER  none among required checks
```

## Minute 2 — prove the blocker model

```bash
aidoc doctor --config examples/broken.example.json
```

The example deliberately fails a required acceptance artifact.

The important output is not a score. It is:

```text
FIRST BLOCKER  missing-acceptance-artifact
```

The CLI also states that this is a triage boundary rather than a proven root cause.

## Minute 3 — prove Agent + deterministic verification can cooperate

The repository includes:

```text
.agents/skills/ai-delivery-doctor/SKILL.md
```

The Skill asks an Agent to understand the expected outcome and write a small ordered contract.

The CLI then verifies observable facts.

That separation is the product:

> **AI decides what needs evidence. Deterministic code establishes what actually happened.**
