# Technical Philosophy

AI Delivery Doctor is based on a simple observation:

> Automation without verifiability can move work from humans into systems while moving uncertainty into operations.

The project therefore treats **verification as part of automation**, not an afterthought.

## 1. Separate interpretation from evidence

Large language models are useful for understanding goals, reading repositories, and proposing what should be verified.

They are not a substitute for checking whether a file exists, a service responds, a credential is configured, or an acceptance condition is actually observed.

The project deliberately combines:

- probabilistic reasoning for **planning**;
- deterministic probes for **evidence**.

## 2. Optimize for the first unsupported transition

Complex systems invite broad speculation.

Ordered contracts force a narrower question:

> Where is the earliest required transition that we currently cannot prove?

That boundary reduces the search space without pretending to know more than the evidence supports.

## 3. Do not average away blockers

Global scores are attractive because they are easy to present.

They can also create false confidence.

One missing required credential can invalidate an entire path regardless of how many unrelated checks pass.

## 4. Keep the durable core below fast-moving AI fashion

MCP, model providers, Agent frameworks, RAG stacks, and orchestration libraries will change.

The durable concepts are:

```text
Target
  → Probe
  → Evidence
  → Assertion
  → Transition
  → Acceptance
```

Technology-specific capabilities should be adapters around those concepts.

## 5. The end state is less manual firefighting

A good FDE/AI delivery engineer solves a field problem.

A mature system then converts the repeated part of that solution into a reusable contract, check, adapter, test, or Skill.

The long-term goal is not to create more debugging work. It is to make repeated delivery failures cheaper to detect and easier to prevent.
