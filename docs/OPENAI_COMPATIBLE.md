# OpenAI-Compatible Check

The `openai-compatible` check is AI Delivery Doctor's first protocol-aware AI check.

It intentionally uses only Python's standard library.

## Local compatible endpoint

```json
{
  "id": "local-model-catalog",
  "stage": "model",
  "type": "openai-compatible",
  "base_url": "http://127.0.0.1:11434/v1",
  "required": true
}
```

## Authenticated endpoint

Keep the key outside the contract:

```json
{
  "id": "provider-catalog",
  "stage": "model",
  "type": "openai-compatible",
  "base_url": "https://api.example.test/v1",
  "api_key_env": "PROVIDER_API_KEY",
  "required": true
}
```

The checker reads `PROVIDER_API_KEY` at runtime and sends it as a Bearer token. The value is never included in evidence.

## Required model

```json
{
  "id": "delivery-model",
  "stage": "model",
  "type": "openai-compatible",
  "base_url": "http://127.0.0.1:11434/v1",
  "model": "qwen3:8b",
  "required": true
}
```

A PASS establishes that the compatible catalog responded with valid JSON and listed the requested model.

It does **not** prove that a generation request will succeed, that quotas are sufficient, or that downstream tools/Agent behavior works. Those are separate transitions.
