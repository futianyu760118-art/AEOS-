"""Validate the machine-readable AEOS Phase 1 registry without third-party packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


BRANCH = "aeos/phase1-v1.1"
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
REQUIRED_SYSTEM_FIELDS = {
    "system_id",
    "module",
    "domain",
    "repository",
    "branch",
    "upstream_commit",
    "owner_ref",
    "environment_ref",
    "lifecycle_state",
    "manifest_ref",
}
REQUIRED_MANIFEST_FIELDS = {
    "system_id",
    "module",
    "domain",
    "repository",
    "branch",
    "upstream_commit",
    "owner_ref",
    "environment_ref",
    "lifecycle_state",
    "health_check",
    "build_command",
    "test_command",
    "rollback_command",
}
RUNTIME_PERSON_LIFECYCLE_SYSTEMS = {
    "M01_KERNEL", "M02_EDP", "M03_EBMS", "M04_PLM", "M05_CRM", "M06_SPC",
    "M07_HLC", "M09_FAC", "M10_POMS", "M13_AEOS_HUB", "M14_NOMI_1", "M14_NOMI",
}


def _load(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load {path}: {exc}") from exc


def _non_empty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_registry(repo_root: Path | str) -> list[str]:
    root = Path(repo_root)
    registry_dir = root / "registry"
    errors: list[str] = []

    try:
        systems_doc = _load(registry_dir / "systems.yaml")
        environments_doc = _load(registry_dir / "environments.yaml")
        owners_doc = _load(registry_dir / "owners.yaml")
        dependencies_doc = _load(registry_dir / "dependencies.yaml")
    except ValueError as exc:
        return [str(exc)]

    try:
        gates_doc = _load(registry_dir / "capability-gates.yaml")
    except ValueError as exc:
        return [str(exc)]
    gates = gates_doc.get("gates") if isinstance(gates_doc, dict) else None
    if not isinstance(gates, list):
        errors.append("capability-gates.yaml must contain a gates list")
        gates = []
    gate_ids = {item.get("system_id") for item in gates if isinstance(item, dict)}
    if gate_ids != {"M08_QUALITY", "M11_INTEGRATION", "M12_DEVSECOPS"}:
        errors.append("capability-gates.yaml must contain M08_QUALITY, M11_INTEGRATION and M12_DEVSECOPS")
    for gate in gates:
        if not isinstance(gate, dict):
            errors.append("capability gate entry must be an object")
            continue
        if gate.get("deployment_state") != "NOT_DEPLOYED":
            errors.append(f"capability gate {gate.get('system_id')} must be NOT_DEPLOYED")

    systems = systems_doc.get("systems") if isinstance(systems_doc, dict) else None
    environments = environments_doc.get("environments") if isinstance(environments_doc, dict) else None
    owners = owners_doc.get("owners") if isinstance(owners_doc, dict) else None
    if not isinstance(systems, list):
        errors.append("systems.yaml must contain a systems list")
        systems = []
    if not isinstance(environments, list):
        errors.append("environments.yaml must contain an environments list")
        environments = []
    if not isinstance(owners, list):
        errors.append("owners.yaml must contain an owners list")
        owners = []
    if not isinstance(dependencies_doc, dict) or not isinstance(dependencies_doc.get("direction"), list):
        errors.append("dependencies.yaml must contain a direction list")

    system_ids: set[str] = set()
    system_by_id: dict[str, dict[str, Any]] = {}
    for index, system in enumerate(systems):
        if not isinstance(system, dict):
            errors.append(f"system entry {index} must be an object")
            continue
        missing = REQUIRED_SYSTEM_FIELDS - system.keys()
        if missing:
            errors.append(f"system entry {index} missing fields: {', '.join(sorted(missing))}")
        system_id = system.get("system_id")
        if system_id in system_ids:
            errors.append(f"duplicate system_id: {system_id}")
        if _non_empty(system_id):
            system_ids.add(system_id)
            system_by_id[system_id] = system
        if system.get("branch") != BRANCH:
            errors.append(f"invalid branch for {system_id}: expected {BRANCH}")
        if not COMMIT_RE.fullmatch(system.get("upstream_commit", "")):
            errors.append(f"missing locked commit for {system_id}")

    environment_ids = {item.get("environment_id") for item in environments if isinstance(item, dict)}
    owner_ids = {item.get("owner_ref") for item in owners if isinstance(item, dict)}
    required_environment_names = {"local", "development", "test", "staging", "production"}
    environment_names = {item.get("name") for item in environments if isinstance(item, dict)}
    for name in sorted(required_environment_names - environment_names):
        errors.append(f"missing environment: {name}")
    for environment in environments:
        if not isinstance(environment, dict):
            errors.append("environment entry must be an object")
            continue
        for field in ("environment_id", "name", "endpoint_ref", "credentials_ref", "certificate_ref", "status"):
            if not _non_empty(environment.get(field)):
                errors.append(f"environment missing {field}")
        if environment.get("credentials_ref", "").startswith("secret:"):
            errors.append(f"credentials must remain external for {environment.get('environment_id')}")

    for owner in owners:
        if not isinstance(owner, dict):
            errors.append("owner entry must be an object")
            continue
        for field in ("owner_ref", "role", "accountable_for", "status"):
            if not _non_empty(owner.get(field)):
                errors.append(f"owner missing {field}")

    manifest_dir = registry_dir / "system-manifests"
    manifests = sorted(manifest_dir.glob("*.yaml")) if manifest_dir.exists() else []
    manifest_ids: set[str] = set()
    for path in manifests:
        try:
            manifest = _load(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not isinstance(manifest, dict):
            errors.append(f"manifest {path.name} must be an object")
            continue
        system_id = manifest.get("system_id")
        if system_id not in system_by_id:
            errors.append(f"unknown system in manifest {path.name}: {system_id}")
        if system_id in manifest_ids:
            errors.append(f"duplicate manifest system_id: {system_id}")
        manifest_ids.add(system_id)
        missing = REQUIRED_MANIFEST_FIELDS - manifest.keys()
        if missing:
            errors.append(f"manifest {path.name} missing fields: {', '.join(sorted(missing))}")
        if manifest.get("branch") != BRANCH:
            errors.append(f"invalid branch in manifest {path.name}")
        if not COMMIT_RE.fullmatch(manifest.get("upstream_commit", "")):
            errors.append(f"missing locked commit in manifest {path.name}")
        for field in ("health_check", "build_command", "test_command", "rollback_command"):
            if not _non_empty(manifest.get(field)):
                errors.append(f"manifest {path.name} missing command: {field}")
        if manifest.get("owner_ref") not in owner_ids:
            errors.append(f"manifest {path.name} references missing owner: {manifest.get('owner_ref')}")
        if manifest.get("environment_ref") not in environment_ids:
            errors.append(f"manifest {path.name} references missing environment: {manifest.get('environment_ref')}")
        if system_id in RUNTIME_PERSON_LIFECYCLE_SYSTEMS:
            for field in ("person_lifecycle_role", "person_lifecycle_endpoint", "sync_capabilities", "deployment_state"):
                value = manifest.get(field)
                if field == "sync_capabilities":
                    if not isinstance(value, list) or not value:
                        errors.append(f"manifest {path.name} missing person lifecycle capabilities")
                elif not _non_empty(value):
                    errors.append(f"manifest {path.name} missing person lifecycle field: {field}")
        registered = system_by_id.get(system_id)
        if registered:
            for field in ("module", "repository", "branch", "upstream_commit", "owner_ref", "environment_ref"):
                if manifest.get(field) != registered.get(field):
                    errors.append(f"manifest {path.name} does not match systems.yaml field: {field}")
        if manifest.get("lifecycle_state") == "READY":
            sign_off = manifest.get("sign_off")
            if not isinstance(sign_off, dict) or sign_off.get("owner") != "APPROVED":
                errors.append(f"READY manifest {path.name} is missing owner sign-off")
            if not isinstance(sign_off, dict) or sign_off.get("environment") != "APPROVED":
                errors.append(f"READY manifest {path.name} is missing environment sign-off")
            owner = next((item for item in owners if item.get("owner_ref") == manifest.get("owner_ref")), None)
            if not owner or owner.get("status") != "APPROVED":
                errors.append(f"READY manifest {path.name} owner is not approved")

    for system_id in sorted(system_ids - manifest_ids):
        errors.append(f"missing manifest for registered system: {system_id}")
    for manifest_id in sorted(manifest_ids - system_ids):
        errors.append(f"unknown system in manifest set: {manifest_id}")

    return errors


def main() -> int:
    errors = validate_registry(Path(__file__).resolve().parents[1])
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("AEOS registry validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
