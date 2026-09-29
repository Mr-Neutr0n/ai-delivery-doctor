# Roadmap

The roadmap is organized around one principle: **keep the evidence/acceptance core stable while technology-specific adapters evolve.**

## v0.1 — Evidence-first foundation

- [x] ordered JSON delivery contracts;
- [x] file / env / executable / TCP / HTTP checks;
- [x] PASS / WARN / FAIL evidence;
- [x] first required blocker;
- [x] JSON evidence;
- [x] Markdown report;
- [x] shareable evidence mode;
- [x] Agent Skill;
- [x] cross-platform CI;
- [x] deterministic Skill packaging;
- [ ] external user validation on at least three environments.

## v0.2 — AI-native adapters

- [x] OpenAI-compatible endpoint adapter;
- [ ] Ollama adapter;
- [ ] MCP server/tool health adapter;
- [ ] Docker/container readiness adapter;
- [ ] reusable acceptance profiles;
- [x] evidence comparison between two runs.

## v0.3 — Delivery workflow

- [ ] plugin/check registration API;
- [ ] baseline vs current evidence diff;
- [ ] machine-readable remediation hints without automatic mutation;
- [ ] richer redaction policies;
- [ ] CI mode for pull requests and deployments;
- [ ] reusable acceptance bundles.

## v0.4 — Agent collaboration

- [ ] contract-generation helpers for coding agents;
- [ ] skill validation in CI;
- [ ] reference skills for common AI delivery paths;
- [ ] adapters contributed by the community.

## v1.0 — Stable acceptance contract

Target only after:

- public contract semantics are documented and proven in multiple real projects;
- plugin API is stable;
- security/redaction behavior is well tested;
- cross-platform behavior is predictable;
- users outside the maintainer's own projects rely on it.

## Deliberate non-goals

- becoming another general Agent framework;
- replacing Langfuse/observability platforms;
- replacing RAG evaluation suites;
- executing arbitrary remediation commands;
- hiding critical blockers inside a global readiness score.
