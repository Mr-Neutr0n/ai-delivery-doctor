# Contract guidance for the AI Delivery Doctor Skill

When an Agent creates an `aidoc-v1` contract, keep it small.

## Prefer

3–8 checks that trace one actual user outcome.

Example:

```text
runtime
  → provider configuration
  → local tool/service
  → workflow endpoint
  → acceptance artifact
```

## Avoid

- giant generic checklists;
- checks unrelated to the user's outcome;
- secret values in JSON;
- arbitrary command execution;
- private endpoints not supplied or authorized by the user;
- claiming a failed probe is automatically the root cause.

## Interpretation

A PASS means only that the specific bounded observation succeeded.

The first required FAIL is the current blocker in the declared path.
