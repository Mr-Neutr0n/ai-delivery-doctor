# FAQ

## Is this another Agent framework?

No. AI Delivery Doctor does not orchestrate agents. It verifies bounded conditions in an AI delivery path and records evidence.

## Is it an observability platform?

No. Observability platforms are excellent for traces, metrics, evaluations, and production monitoring. AI Delivery Doctor focuses on explicit delivery/acceptance contracts and the first required transition that cannot be proven.

## Why not give a readiness score?

Because one critical required failure can invalidate a delivery path even when many unrelated checks pass. The project reports evidence and the first blocker instead of averaging it away.

## Does PASS mean the whole AI application works?

No. PASS means only the bounded observation performed by that check succeeded.

For example:

- TCP PASS proves a connection was established;
- HTTP PASS proves an accepted HTTP status was returned;
- OpenAI-compatible PASS proves a valid model catalog (and optionally a requested model) was observed.

None of those automatically proves downstream Agent behavior or user outcomes.

## Why use an Agent Skill if the checks are deterministic?

The Agent handles semantic work: understand the user's goal, inspect the project, and decide which transitions should be verified.

The deterministic core handles factual observations.

## Does the tool modify production systems?

The v0.1 core is read-only. It does not restart services, edit configuration, rotate keys, build containers, or execute arbitrary shell commands from contracts.

## Can I use it in CI?

Yes. `aidoc doctor` exits non-zero on a required blocker. `aidoc compare` exits non-zero when a required check regresses.

## Can it check private services?

It can probe explicitly supplied targets, but users are responsible for authorization. Use `--shareable` before moving evidence outside the deployment environment and review output manually.

## Why is EdgeSafe Vision mentioned?

EdgeSafe Vision is one real engineering source of the project's evidence-first philosophy. It exposed a recurring pattern: upstream components can appear healthy while the final operator outcome still fails. AI Delivery Doctor generalizes that pattern beyond edge computer vision.

## What should contributors build next?

See issues labeled `good first issue`, `help wanted`, and [ROADMAP.md](../ROADMAP.md). The project especially welcomes protocol-aware adapters that preserve the core Target → Probe → Evidence → Acceptance model.
