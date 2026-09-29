# AI Delivery Doctor

[![CI](https://github.com/Yazhou-Li/ai-delivery-doctor/actions/workflows/ci.yml/badge.svg)](https://github.com/Yazhou-Li/ai-delivery-doctor/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/Yazhou-Li/ai-delivery-doctor)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](pyproject.toml)

> **Evidence-first acceptance checks for AI applications. Find the first unsupported transition before your customer does.**

AI Delivery Doctor (`aidoc`) is a local-first, dependency-light CLI + Agent Skill for the last mile between **"the AI demo works"** and **"the delivered system can be verified."**

It does not try to replace observability platforms, RAG evaluation frameworks, MCP analyzers, or deployment platforms. Its job is narrower:

**define a delivery chain → run bounded checks → preserve evidence → stop at the first required transition that cannot be proven.**

## Why this exists

AI delivery failures often happen outside the model:

- a runtime, file, credential, or service is missing;
- an API is reachable from one machine but not another;
- an MCP/tool service does not start;
- a downstream workflow is assumed healthy because an upstream endpoint returned `200`;
- teams have logs, but no small acceptance contract that says what must be true before handoff.

AI Delivery Doctor treats delivery as an **ordered acceptance contract**, not a vague readiness score.

```text
human / Agent
     ↓
delivery contract (JSON)
     ↓
bounded deterministic probes
     ↓
PASS / WARN / FAIL evidence
     ↓
first required blocker
     ↓
next verification step
```

## Quick start

```bash
git clone https://github.com/Yazhou-Li/ai-delivery-doctor.git
cd ai-delivery-doctor

python -m pip install -e .
python -m unittest discover -s tests -v

aidoc doctor --config examples/acceptance.example.json
aidoc doctor --config examples/broken.example.json
```

The first example passes all required checks. The second intentionally fails one required acceptance artifact so you can see the blocking behavior.

For the full before → repair condition → after → evidence-diff story in one command:

```bash
python scripts/showcase.py
```

See [3-Minute Showcase](docs/SHOWCASE.md) and the [Chinese hackathon walkthrough](docs/HACKATHON_CN.md).

## Core commands

```bash
aidoc init --output aidoc.json
aidoc validate --config aidoc.json

aidoc doctor \
  --config aidoc.json \
  --json evidence.json \
  --markdown report.md

aidoc doctor \
  --config aidoc.json \
  --json shareable-evidence.json \
  --shareable

aidoc compare baseline.json current.json \
  --markdown comparison.md
```

## Supported v0.1 checks

| Type | What it proves |
|---|---|
| `file` | a required readable file exists |
| `env` | an environment variable exists; its value is never printed |
| `executable` | an executable is available on `PATH` |
| `tcp` | a TCP connection can be established |
| `http` | an HTTP endpoint returns an accepted status |
| `openai-compatible` | a `/v1/models`-style catalog is reachable and optionally contains a required model |

Evidence bundles can also be compared across deployments or fixes. A required status regression makes `aidoc compare` exit non-zero, which makes it useful in CI and acceptance workflows.

The core deliberately does **not** execute arbitrary shell commands from a contract.

## Example contract

```json
{
  "schema": "aidoc-v1",
  "name": "local-ai-service",
  "checks": [
    {
      "id": "python-runtime",
      "stage": "environment",
      "type": "executable",
      "name": "python",
      "required": true
    },
    {
      "id": "project-config",
      "stage": "environment",
      "type": "file",
      "path": "../pyproject.toml",
      "required": true
    },
    {
      "id": "optional-provider-key",
      "stage": "model",
      "type": "env",
      "name": "OPENAI_API_KEY",
      "required": false
    }
  ]
}
```

Check order is meaningful. AI Delivery Doctor reports the first failed **required** check as the current blocking transition.

That is a **triage boundary**, not a claim that the check is the ultimate root cause.

## Why there is no 0–100 readiness score

A project with nine green checks and one broken required credential is not "90% ready" for the affected delivery path.

AI Delivery Doctor reports evidence, counts, and the first required blocker instead of hiding critical failures inside a global score.

## Agent Skill

A portable Agent Skill lives at:

```text
.agents/skills/ai-delivery-doctor/
```

The Skill handles the semantic part of the workflow:

1. define the expected user outcome;
2. inspect the project and identify the smallest meaningful delivery chain;
3. create/refine an `aidoc-v1` contract;
4. run deterministic checks;
5. interpret the first unsupported transition without inventing a root cause.

Package it for sharing:

```bash
python scripts/package_skill.py .agents/skills/ai-delivery-doctor
```

## Design philosophy

**Reasoning may be probabilistic. Acceptance evidence should be deterministic.**

The long-lived core is intentionally vendor-neutral:

```text
Target → Probe → Evidence → Assertion → Transition → Acceptance
```

MCP, RAG, Ollama, OpenAI-compatible APIs, browser agents, Docker, Kubernetes, and edge AI should be adapters around that core—not the foundation of the project.

The first AI-native adapter is now built in: `openai-compatible` checks the model catalog directly, reads API keys only from environment variables, and never writes key values into evidence.

## Safety

- no secret values in reports;
- URL credentials/query/fragment are removed from HTTP labels;
- `--shareable` further minimizes operator-supplied details;
- no automatic restarts or configuration changes;
- no arbitrary shell execution;
- no claim that network reachability proves downstream business behavior.

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## Contributing

Small, evidence-driven contributions are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md), then look for issues labeled `good first issue` or `help wanted`.

## License

Apache-2.0.
