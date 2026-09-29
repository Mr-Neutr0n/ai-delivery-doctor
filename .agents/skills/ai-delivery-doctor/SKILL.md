---
name: ai-delivery-doctor
description: Turn an AI application's vague delivery or deployment uncertainty into an explicit ordered acceptance contract, deterministic checks, evidence, and the first unsupported required transition. Use when an Agent, RAG, MCP, model API, automation, or AI application works as a demo but needs to be verified for handoff, deployment, troubleshooting, or customer acceptance.
license: Apache-2.0
compatibility: Requires Python 3.10+ and the local ai-delivery-doctor package. Network probes must be limited to operator-approved or repository-documented endpoints.
metadata:
  author: Yazhou Li
  version: "0.1.0"
---

# AI Delivery Doctor

Use this skill when the problem is not "write another AI feature" but "prove the delivery chain works far enough to hand off safely."

## Core principle

Separate two jobs:

- **Reasoning job:** understand the expected user outcome and decide which transitions need evidence.
- **Verification job:** let deterministic probes establish observable facts.

Do not let model confidence substitute for evidence.

## Workflow

1. Write the expected outcome in one sentence.
2. Write the observed outcome in one sentence.
3. Inspect the repository and identify the smallest ordered delivery chain that matters.
4. Create or update an `aidoc-v1` JSON contract.
5. Use only bounded checks supported by the CLI:
   - file
   - env
   - executable
   - tcp
   - http
6. Never put secret values in the contract.
7. Only probe network targets that the user supplied or the project already documents for local/testing use.
8. Run:
   ```bash
   aidoc doctor --config <contract.json> --json evidence.json --markdown report.md
   ```
9. Read results in order.
10. Stop at the first failed required check. Treat it as the first unsupported transition, not automatically as the root cause.
11. Propose one next verification step that can distinguish the most plausible causes.
12. Do not mutate services, rotate credentials, change firewalls, or edit production configuration unless the user separately requests remediation.

## Contract design

Prefer 3–8 checks that trace a real outcome. Do not create a giant checklist just to look comprehensive.

Useful stages include:

- environment
- model
- tools
- data
- workflow
- deployment
- operator
- acceptance

Stage names are descriptive; check order defines the delivery path.

## Evidence rules

- PASS proves only the bounded check that ran.
- WARN is not success.
- A reachable TCP port does not prove the protocol or business action works.
- HTTP 401/403 proves reachability but not successful application behavior.
- An environment-variable check never prints its value.
- A passing upstream step never proves a downstream user outcome.

## Completion

Finish with:

- expected outcome;
- observed outcome;
- contract used;
- PASS/WARN/FAIL evidence;
- first blocking transition;
- one next verification step;
- what was intentionally not tested.
