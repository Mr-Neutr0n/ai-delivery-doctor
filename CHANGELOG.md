# Changelog

All notable changes to AI Delivery Doctor are documented here.

## Unreleased

### Added

- community contribution and support documentation;
- reproducible one-command before/after showcase;
- contract reference and public `aidoc-v1` JSON Schema;
- EdgeSafe Vision case-study bridge;
- evidence comparison with required-regression exit semantics;
- OpenAI-compatible model catalog check;
- real loopback HTTP/TCP/OpenAI-compatible integration test;
- `python -m aidoc` entry point;
- deterministic Agent Skill artifact workflow;
- dependency-free Agent Skill validation;
- GitHub issue forms, PR template, and CODEOWNERS.

### Changed

- GitHub Actions upgraded to the current Node 24 generation;
- Agent Skill packaging now validates the Skill before publishing an artifact.

## 0.1.0 — 2026-09-29

### Added

- `aidoc init`, `aidoc validate`, and `aidoc doctor`;
- ordered `aidoc-v1` delivery contracts;
- file, env, executable, TCP, and HTTP checks;
- first required blocking transition;
- JSON evidence and Markdown report output;
- shareable evidence mode;
- portable Agent Skill;
- deterministic Skill zip packaging;
- Linux, Windows, and macOS CI.
