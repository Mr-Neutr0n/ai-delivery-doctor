# Community Outreach Guide

## Goal

Help more AI engineers discover, evaluate, and contribute to AI Delivery Doctor while keeping the project focused on evidence-driven AI delivery acceptance.

## Who to reach

- AI application engineers
- Agent / MCP developers
- FDE and solution engineers
- DevOps and platform engineers
- Open-source contributors interested in AI reliability

## Outreach principles

- Do not spam users.
- Share only with communities where the project is relevant.
- Invite discussion before asking for contributions.
- Never claim production certification or guaranteed reliability.

## Suggested introduction

> Hi, we are building AI Delivery Doctor, an open-source toolkit for evidence-first acceptance checks for AI applications. The goal is to help teams move from "the demo works" to "the delivery can be verified" through deterministic contracts, bounded checks, and evidence bundles.
>
> If you work on AI agents, MCP, RAG, or AI application delivery, we would appreciate feedback on the design. Small documentation, examples, tests, and reproducible cases are welcome.

## Safe contribution path

1. Read CONTRIBUTING.md.
2. Start with documentation, examples, or good-first issues.
3. Keep changes small and testable.
4. Avoid secrets, customer data, private endpoints, and production assumptions.

## Maintainer review checklist

Before merging:

- Does this preserve evidence-first design?
- Does it avoid hidden side effects?
- Are tests included?
- Is scope clearly documented?
- Does it improve real user value?
