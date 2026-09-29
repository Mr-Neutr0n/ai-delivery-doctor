# Contributing

Thanks for helping improve AI Delivery Doctor.

The project favors **small, evidence-driven contributions** that make AI delivery easier to verify, diagnose, and hand off.

## Good contribution areas

- new deterministic check types;
- safer evidence redaction;
- report formats;
- contract validation;
- model/MCP/RAG/Docker adapters that preserve the core evidence model;
- cross-platform behavior;
- reproducible examples;
- documentation and onboarding;
- regression tests from real delivery failures.

## Development setup

```bash
git clone https://github.com/Yazhou-Li/ai-delivery-doctor.git
cd ai-delivery-doctor
python -m pip install -e .
python -m unittest discover -s tests -v
```

## Before submitting code

1. Read [AGENTS.md](AGENTS.md).
2. Keep changes narrowly scoped.
3. Add or update tests for behavior changes.
4. Use synthetic/local fixtures.
5. Never include secret values, private customer endpoints, private IPs, or production logs.
6. Do not add arbitrary shell execution to contracts.
7. Do not turn a failed probe into a definitive root-cause claim.
8. Update docs when public behavior changes.

## Check design

A good check:

- makes one bounded observation;
- has explicit inputs;
- produces PASS/WARN/FAIL with a narrow meaning;
- is read-only by default;
- avoids leaking secrets;
- is deterministic enough to test;
- does not pretend to prove downstream behavior it did not observe.

## Adapter design

Technology-specific integrations belong around the durable core.

Prefer:

```text
specific technology
      ↓
adapter/check
      ↓
CheckResult / Evidence
      ↓
ordered delivery contract
```

Avoid coupling the core model to one Agent framework, model provider, MCP client, RAG library, or cloud.

## Pull requests

A good PR should make it easy to answer:

1. What real delivery problem does this solve?
2. What observable fact does it establish?
3. What changed?
4. How was it verified?
5. What does the result **not** prove?
6. Does it preserve privacy and read-only defaults?

If the requested behavior is ambiguous, choose the smallest reviewable interpretation and state the assumption.
