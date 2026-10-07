# aidoc-v1 Contract Reference

An AI Delivery Doctor contract is a JSON object describing an ordered set of bounded checks.

## Root object

```json
{
  "schema": "aidoc-v1",
  "name": "my-delivery-path",
  "checks": []
}
```

- `schema` must be exactly `aidoc-v1`.
- `name` is a non-empty human-readable name.
- `checks` is a non-empty ordered array.

Check order is semantically meaningful.

## Common check fields

Every check requires:

- `id`: unique non-empty string;
- `stage`: descriptive stage such as `environment`, `model`, `tools`, `data`, `workflow`, `operator`, or `acceptance`;
- `type`: one of the supported check types;
- `required`: boolean, default `true`.

A missing/failed optional check becomes WARN rather than a required blocker.

## directory

```json
{
  "id": "model-cache-dir",
  "stage": "environment",
  "type": "directory",
  "path": "./models",
  "required": true
}
```

Relative paths are resolved from the directory containing the contract.

PASS requires the path to exist and be a directory. The check does not create or modify paths.

## file

```json
{
  "id": "config",
  "stage": "environment",
  "type": "file",
  "path": "./config.json",
  "required": true
}
```

Relative paths are resolved from the directory containing the contract.

## env

```json
{
  "id": "provider-key",
  "stage": "model",
  "type": "env",
  "name": "OPENAI_API_KEY",
  "required": true
}
```

The value is never printed.

## executable

```json
{
  "id": "docker-cli",
  "stage": "environment",
  "type": "executable",
  "name": "docker",
  "required": false
}
```

## tcp

```json
{
  "id": "local-service-port",
  "stage": "deployment",
  "type": "tcp",
  "host": "127.0.0.1",
  "port": 8000,
  "timeout": 2.0,
  "required": true
}
```

PASS proves only that a TCP connection was established.

## http

```json
{
  "id": "health-endpoint",
  "stage": "deployment",
  "type": "http",
  "url": "http://127.0.0.1:8000/health",
  "accept_status": [200],
  "timeout": 3.0,
  "required": true
}
```

URL credentials, query strings, and fragments are removed from diagnostic labels.

A 401/403 is reported as WARN reachability evidence unless explicitly included in `accept_status`.

## First blocker semantics

The first required FAIL is the current **blocking transition**.

It is not automatically the root cause. It is the earliest point in the declared path where the expected condition could not be established.


## openai-compatible

Use this check for an OpenAI-compatible model catalog, including compatible local gateways.

```json
{
  "id": "model-catalog",
  "stage": "model",
  "type": "openai-compatible",
  "base_url": "http://127.0.0.1:11434/v1",
  "model": "qwen3:8b",
  "required": true
}
```

For authenticated endpoints, reference an environment-variable **name**, never the key value:

```json
{
  "id": "provider",
  "stage": "model",
  "type": "openai-compatible",
  "base_url": "https://api.example.test/v1",
  "api_key_env": "PROVIDER_API_KEY",
  "required": true
}
```

The check calls `/models`, validates the JSON `data` array, and optionally confirms that a requested model ID exists.

The API key value is never written to the contract, terminal output, or evidence.
