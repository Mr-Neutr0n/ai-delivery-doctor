from __future__ import annotations

import hashlib
import os
import shutil
import socket
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit

from .config import DeliveryConfig
from .model import CheckResult, CheckSpec


def _status_for_missing(spec: CheckSpec) -> str:
    return "FAIL" if spec.required else "WARN"


def _result(spec: CheckSpec, status: str, detail: str) -> CheckResult:
    return CheckResult(
        spec.check_id,
        spec.stage,
        spec.check_type,
        spec.required,
        status,
        detail,
    )


def _missing(spec: CheckSpec, detail: str) -> CheckResult:
    return _result(spec, _status_for_missing(spec), detail)


def _string_option(spec: CheckSpec, key: str) -> str:
    value = spec.options.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{spec.check_id}.{key} must be a non-empty string")
    return value.strip()


def _safe_url_label(url: str) -> str:
    try:
        parsed = urlsplit(url)
        host = parsed.hostname or ""
        if ":" in host and not host.startswith("["):
            host = f"[{host}]"
        if parsed.port is not None:
            host = f"{host}:{parsed.port}"
        return urlunsplit((parsed.scheme, host, parsed.path, "", ""))
    except ValueError:
        return url.split("?", 1)[0].split("#", 1)[0]


def _alias(value: str, prefix: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:8]
    return f"{prefix}-{digest}"


def sanitize_result(result: CheckResult) -> CheckResult:
    """Minimize operator-supplied details while preserving diagnostic meaning."""

    detail = result.detail

    if result.check_type == "file":
        detail = (
            "file check passed"
            if result.status == "PASS"
            else "file check did not establish the expected condition"
        )
    elif result.check_type == "env":
        detail = (
            "environment variable is set"
            if result.status == "PASS"
            else "environment variable is not set"
        )
    elif result.check_type == "executable":
        detail = (
            "executable is available"
            if result.status == "PASS"
            else "executable is not available"
        )
    elif result.check_type == "tcp":
        detail = (
            "TCP connection established to " + _alias(result.check_id, "target")
            if result.status == "PASS"
            else "TCP connection failed for " + _alias(result.check_id, "target")
        )
    elif result.check_type in {"http", "openai-compatible"}:
        code = ""
        for token in detail.replace(":", " ").split():
            if token.isdigit() and len(token) == 3:
                code = token
                break
        detail = "HTTP probe result" + (f": {code}" if code else "")

    return CheckResult(
        result.check_id,
        result.stage,
        result.check_type,
        result.required,
        result.status,
        detail,
    )


def check_file(spec: CheckSpec, base_dir: Path) -> CheckResult:
    value = _string_option(spec, "path")
    raw_path = Path(value)
    target = (
        (base_dir / raw_path).resolve()
        if not raw_path.is_absolute()
        else raw_path.expanduser().resolve()
    )

    if not target.exists():
        return _missing(spec, f"required path not found: {value}")
    if not target.is_file():
        return _missing(spec, f"path is not a regular file: {value}")

    try:
        size = target.stat().st_size
        with target.open("rb") as handle:
            handle.read(1)
    except OSError as exc:
        return _missing(spec, f"{type(exc).__name__}: {exc}")

    return _result(spec, "PASS", f"readable file ({size} bytes): {value}")


def check_env(spec: CheckSpec) -> CheckResult:
    name = _string_option(spec, "name")
    if os.environ.get(name):
        return _result(spec, "PASS", f"environment variable is set: {name}")
    return _missing(spec, f"environment variable is not set: {name}")


def check_executable(spec: CheckSpec) -> CheckResult:
    name = _string_option(spec, "name")
    if not shutil.which(name):
        return _missing(spec, f"executable not found on PATH: {name}")
    return _result(spec, "PASS", f"executable available: {name}")


def check_tcp(spec: CheckSpec) -> CheckResult:
    host = _string_option(spec, "host")
    port = spec.options.get("port")
    if (
        isinstance(port, bool)
        or not isinstance(port, int)
        or not (1 <= port <= 65535)
    ):
        raise ValueError(
            f"{spec.check_id}.port must be an integer from 1 to 65535"
        )

    timeout = spec.options.get("timeout", 2.0)
    if (
        isinstance(timeout, bool)
        or not isinstance(timeout, (int, float))
        or timeout <= 0
    ):
        raise ValueError(f"{spec.check_id}.timeout must be a positive number")

    try:
        with socket.create_connection((host, port), timeout=float(timeout)):
            return _result(
                spec,
                "PASS",
                f"TCP connection established: {host}:{port}",
            )
    except OSError as exc:
        return _missing(
            spec,
            f"TCP connection failed: {host}:{port} ({type(exc).__name__})",
        )


def check_http(spec: CheckSpec) -> CheckResult:
    url = _string_option(spec, "url")
    label = _safe_url_label(url)

    timeout = spec.options.get("timeout", 3.0)
    if (
        isinstance(timeout, bool)
        or not isinstance(timeout, (int, float))
        or timeout <= 0
    ):
        raise ValueError(f"{spec.check_id}.timeout must be a positive number")

    raw_accept = spec.options.get("accept_status")
    if raw_accept is None:
        accepted = set(range(200, 400))
    elif (
        isinstance(raw_accept, list)
        and raw_accept
        and all(
            isinstance(value, int)
            and not isinstance(value, bool)
            and 100 <= value <= 599
            for value in raw_accept
        )
    ):
        accepted = set(raw_accept)
    else:
        raise ValueError(
            f"{spec.check_id}.accept_status must be a non-empty array "
            "of HTTP status integers"
        )

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "AI-Delivery-Doctor/0.1"},
    )

    try:
        with urllib.request.urlopen(req, timeout=float(timeout)) as response:
            code = int(getattr(response, "status", 200))
    except urllib.error.HTTPError as exc:
        code = exc.code
    except Exception as exc:
        return _missing(
            spec,
            f"HTTP probe failed: {label} ({type(exc).__name__})",
        )

    if code in accepted:
        return _result(spec, "PASS", f"HTTP {code}: {label}")

    if code in (401, 403):
        return _result(
            spec,
            "WARN",
            f"reachable but authentication/authorization required: "
            f"HTTP {code} {label}",
        )

    return _missing(spec, f"unexpected HTTP {code}: {label}")


def check_openai_compatible(spec: CheckSpec) -> CheckResult:
    """Verify an OpenAI-compatible /models catalog without using an SDK."""

    base_url = _string_option(spec, "base_url")
    models_url = urljoin(base_url.rstrip("/") + "/", "models")
    label = _safe_url_label(models_url)

    timeout = spec.options.get("timeout", 5.0)
    if (
        isinstance(timeout, bool)
        or not isinstance(timeout, (int, float))
        or timeout <= 0
    ):
        raise ValueError(f"{spec.check_id}.timeout must be a positive number")

    headers = {"User-Agent": "AI-Delivery-Doctor/0.1"}
    api_key_env = spec.options.get("api_key_env")

    if api_key_env is not None:
        if not isinstance(api_key_env, str) or not api_key_env.strip():
            raise ValueError(
                f"{spec.check_id}.api_key_env must be a non-empty string"
            )
        api_key = os.environ.get(api_key_env.strip())
        if not api_key:
            return _missing(
                spec,
                f"API key environment variable is not set: "
                f"{api_key_env.strip()}",
            )
        headers["Authorization"] = f"Bearer {api_key}"

    requested_model = spec.options.get("model")
    if requested_model is not None and (
        not isinstance(requested_model, str)
        or not requested_model.strip()
    ):
        raise ValueError(
            f"{spec.check_id}.model must be a non-empty string when provided"
        )

    request = urllib.request.Request(models_url, headers=headers)

    try:
        with urllib.request.urlopen(
            request,
            timeout=float(timeout),
        ) as response:
            code = int(getattr(response, "status", 200))
            raw = response.read()
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            return _missing(
                spec,
                f"OpenAI-compatible authentication failed: "
                f"HTTP {exc.code} {label}",
            )
        return _missing(
            spec,
            f"OpenAI-compatible catalog returned HTTP {exc.code}: {label}",
        )
    except Exception as exc:
        return _missing(
            spec,
            f"OpenAI-compatible probe failed: "
            f"{label} ({type(exc).__name__})",
        )

    if not (200 <= code < 300):
        return _missing(
            spec,
            f"OpenAI-compatible catalog returned HTTP {code}: {label}",
        )

    try:
        import json

        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return _missing(
            spec,
            f"OpenAI-compatible /models response was not valid JSON: {label}",
        )

    if not isinstance(payload, dict) or not isinstance(
        payload.get("data"),
        list,
    ):
        return _missing(
            spec,
            f"OpenAI-compatible /models response lacks a data array: {label}",
        )

    model_ids = {
        item.get("id")
        for item in payload["data"]
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }

    if requested_model is not None:
        requested_model = requested_model.strip()
        if requested_model not in model_ids:
            return _missing(
                spec,
                f"requested model not present in catalog: {requested_model}",
            )
        return _result(
            spec,
            "PASS",
            f"OpenAI-compatible model available: {requested_model}",
        )

    return _result(
        spec,
        "PASS",
        f"OpenAI-compatible catalog reachable: "
        f"{label} ({len(model_ids)} models)",
    )


def run_check(spec: CheckSpec, config: DeliveryConfig) -> CheckResult:
    if spec.check_type == "file":
        return check_file(spec, config.base_dir)
    if spec.check_type == "env":
        return check_env(spec)
    if spec.check_type == "executable":
        return check_executable(spec)
    if spec.check_type == "tcp":
        return check_tcp(spec)
    if spec.check_type == "http":
        return check_http(spec)
    if spec.check_type == "openai-compatible":
        return check_openai_compatible(spec)
    raise ValueError(f"unsupported check type: {spec.check_type}")


def run_checks(
    config: DeliveryConfig,
    *,
    shareable: bool = False,
) -> list[CheckResult]:
    results = [run_check(spec, config) for spec in config.checks]
    if shareable:
        return [sanitize_result(result) for result in results]
    return results
