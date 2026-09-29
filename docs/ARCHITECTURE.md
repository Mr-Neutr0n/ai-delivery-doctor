# Architecture

AI Delivery Doctor is built around one durable distinction:

> **Semantic planning can be flexible; acceptance evidence should be deterministic.**

## Core invariants

Frameworks, model providers, agent runtimes, and protocols will change. The long-lived layer is:

1. a delivery has an expected user outcome;
2. that outcome depends on a chain of transitions;
3. each important transition needs observable evidence;
4. evidence should be bounded, reproducible, and safe to share;
5. the earliest required transition that cannot be proven is the current debugging boundary.

## v0.1 model

```text
DeliveryConfig
  └── ordered CheckSpec[]
        ├── file
        ├── env
        ├── executable
        ├── tcp
        └── http

CheckSpec
   ↓
CheckResult
   ↓
evidence bundle
   ↓
terminal / Markdown report
```

## Why no global score

A score can hide the difference between cosmetic gaps and one fatal transition.

A project with nine green checks and one required broken credential is not "90% ready" for the affected path.

v0.1 therefore reports counts and the first failed required check instead of inventing a production-readiness number.

## Future adapter boundary

Technology-specific checks should remain adapters around the durable core:

- OpenAI-compatible model endpoints
- Ollama
- MCP servers/tools
- RAG retrieval/evaluation
- Docker/Kubernetes
- browser/computer-use agents
- edge AI
- enterprise identity/policy

The core evidence schema and blocking semantics should not depend on any one of them.

## Relationship with AI agents

An Agent is good at interpreting context and deciding **what should be verified**.

The Doctor core is responsible for **what was actually observed**.

That separation lets the project benefit from better models over time without turning model confidence into acceptance evidence.
