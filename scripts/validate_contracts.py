"""Validate the versioned AEOS Phase 1 contract source package."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


EXPECTED_SCHEMAS = {
    "principal-context-v1.schema.json": {"tenant_id", "source_system", "person_id", "trace_id", "idempotency_key"},
    "system-manifest-v1.schema.json": {"system_code", "module_id", "display_name", "base_url", "health_url", "version"},
    "audit-event-v1.schema.json": {"tenant_id", "event_id", "event_type", "source_system", "object_id", "revision", "trace_id", "idempotency_key"},
    "business-event-v1.schema.json": {"tenant_id", "event_id", "event_type", "source_system", "object_id", "revision", "trace_id", "idempotency_key"},
    "finance-result-v1.schema.json": {"tenant_id", "result_id", "source_system", "object_id", "revision", "status", "evidence_refs"},
    "lead-intake-v1.schema.json": {"contract_version", "intake_id", "source_system", "submitted_at", "contact", "consent", "idempotency_key"},
    "person-lifecycle-event-v1.schema.json": {"tenant_id", "event_id", "event_type", "event_version", "source_system", "object_type", "object_id", "revision", "occurred_at", "effective_at", "correlation_id", "trace_id", "idempotency_key", "person", "status"},
    "person-lifecycle-result-v1.schema.json": {"event_id", "target_system", "status", "changed", "received_at"},
}
SCHEMA_VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_KEY_RE = re.compile(r"^(password|secret|api[_-]?key)$", re.IGNORECASE)


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load JSON {path}: {exc}") from exc


def load_schemas(repo_root: Path | str) -> dict[str, dict[str, Any]]:
    schema_dir = Path(repo_root) / "contracts" / "v1"
    schemas: dict[str, dict[str, Any]] = {}
    for path in sorted(schema_dir.glob("*.schema.json")):
        data = _load_json(path)
        if not isinstance(data, dict):
            raise ValueError(f"schema {path.name} must be an object")
        schemas[path.name] = data
    return schemas


def _contains_forbidden_key(value: Any) -> bool:
    if isinstance(value, dict):
        return any(FORBIDDEN_KEY_RE.fullmatch(str(key)) or _contains_forbidden_key(item) for key, item in value.items())
    if isinstance(value, list):
        return any(_contains_forbidden_key(item) for item in value)
    return False


def validate_contracts(repo_root: Path | str) -> list[str]:
    root = Path(repo_root)
    errors: list[str] = []
    schema_dir = root / "contracts" / "v1"
    try:
        schemas = load_schemas(root)
    except ValueError as exc:
        return [str(exc)]

    missing = set(EXPECTED_SCHEMAS) - set(schemas)
    extra = set(schemas) - set(EXPECTED_SCHEMAS)
    if missing:
        errors.append(f"missing schemas: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"unexpected schemas: {', '.join(sorted(extra))}")

    ids: set[str] = set()
    versions: set[str] = set()
    for name, schema in schemas.items():
        required = schema.get("required")
        if not isinstance(required, list):
            errors.append(f"{name} required must be a list")
            required = []
        missing_required = EXPECTED_SCHEMAS.get(name, set()) - set(required)
        if missing_required:
            errors.append(f"{name} missing required metadata: {', '.join(sorted(missing_required))}")
        if not isinstance(schema.get("$id"), str) or not schema["$id"].strip():
            errors.append(f"{name} must declare a stable $id")
        elif schema["$id"] in ids:
            errors.append(f"duplicate schema $id: {schema['$id']}")
        else:
            ids.add(schema["$id"])
        version = schema.get("schema_version")
        if not isinstance(version, str) or not SCHEMA_VERSION_RE.fullmatch(version):
            errors.append(f"{name} must declare schema_version MAJOR.MINOR.PATCH")
        elif version in versions:
            errors.append(f"duplicate schema version: {version}")
        else:
            versions.add(version)
        for field in ("title", "type"):
            if not isinstance(schema.get(field), str) or not schema[field].strip():
                errors.append(f"{name} missing {field}")
        if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
            errors.append(f"{name} envelope must set additionalProperties to false")
        if _contains_forbidden_key(schema):
            errors.append(f"{name} contains credential field")

    manifest_path = root / "contracts" / "manifest.json"
    try:
        manifest = _load_json(manifest_path)
    except ValueError as exc:
        return errors + [str(exc)]
    if not isinstance(manifest, dict):
        return errors + ["contracts/manifest.json must be an object"]
    entries = manifest.get("schemas")
    if not isinstance(entries, list):
        return errors + ["contracts/manifest.json schemas must be a list"]
    if not isinstance(manifest.get("compatibility_policy"), dict):
        errors.append("manifest missing compatibility_policy")
    if not isinstance(manifest.get("generator"), dict):
        errors.append("manifest missing generator metadata")

    registered: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("manifest schema entry must be an object")
            continue
        name = entry.get("name")
        if name in registered:
            errors.append(f"duplicate manifest schema: {name}")
        registered.add(name)
        if name not in EXPECTED_SCHEMAS:
            errors.append(f"manifest references unknown schema: {name}")
            continue
        if entry.get("version") != schemas.get(name, {}).get("schema_version"):
            errors.append(f"version mismatch for {name}")
        fingerprint = entry.get("sha256")
        if not isinstance(fingerprint, str) or not SHA256_RE.fullmatch(fingerprint):
            errors.append(f"invalid fingerprint for {name}")
        else:
            actual = hashlib.sha256((schema_dir / name).read_bytes()).hexdigest()
            if fingerprint != actual:
                errors.append(f"fingerprint mismatch for {name}")
    if registered != set(EXPECTED_SCHEMAS):
        errors.append("manifest does not register exactly the Phase 1 schemas")
    return errors


def main() -> int:
    errors = validate_contracts(Path(__file__).resolve().parents[1])
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("AEOS contract validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
