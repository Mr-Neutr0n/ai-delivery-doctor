# Using evidence comparison in CI

AI Delivery Doctor can compare two evidence bundles and return a non-zero exit code when a **required** check regresses.

## Example

Capture a known baseline:

```bash
aidoc doctor \
  --config aidoc.json \
  --json baseline.json
```

After a change or deployment:

```bash
aidoc doctor \
  --config aidoc.json \
  --json current.json

aidoc compare baseline.json current.json \
  --markdown comparison.md
```

A required transition changing from PASS → WARN/FAIL, or WARN → FAIL, is reported as REGRESSED.

The comparison does not claim why the regression happened. It narrows the delivery path that needs investigation.
