# Getting Started

## 1. Requirements

- Python 3.10+
- Windows, macOS, or Linux
- no model API key is required for the built-in examples

## 2. Install

```bash
git clone https://github.com/Yazhou-Li/ai-delivery-doctor.git
cd ai-delivery-doctor
python -m pip install -e .
```

## 3. Verify the project itself

```bash
python -m unittest discover -s tests -v
aidoc validate --config examples/acceptance.example.json
aidoc doctor --config examples/acceptance.example.json
```

The passing example intentionally treats `OPENAI_API_KEY` as optional, so a missing key appears as WARN rather than blocking the run.

## 4. See a blocker

```bash
aidoc doctor --config examples/broken.example.json
```

The example contains a missing required artifact. The CLI exits with code 1 and reports it as the first required blocker.

## 5. Create your own contract

```bash
aidoc init --output aidoc.json
```

Edit the generated file so its ordered checks trace one real user outcome.

Prefer a small chain over a giant checklist.

## 6. Produce evidence

```bash
aidoc doctor \
  --config aidoc.json \
  --json evidence.json \
  --markdown report.md
```

For evidence intended to leave the deployment environment:

```bash
aidoc doctor \
  --config aidoc.json \
  --json evidence.shareable.json \
  --markdown report.shareable.md \
  --shareable
```

Review any evidence before external sharing.

## 7. Render a report from stored evidence

To produce a Markdown report from an existing `aidoc-evidence-v1` bundle without re-running checks:

```bash
aidoc report evidence.json --markdown report.md
```

## 8. Use the Agent Skill

The skill is located at:

```text
.agents/skills/ai-delivery-doctor/
```

Package it:

```bash
python scripts/package_skill.py .agents/skills/ai-delivery-doctor
```

The generated archive can be imported into a compatible Agent environment that supports the Agent Skills format.
