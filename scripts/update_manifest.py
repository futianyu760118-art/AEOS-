"""Regenerate ``contracts/manifest.json`` fingerprints from the schema files.

The manifest is a lock file: every ``contracts/v1/*.schema.json`` carries a
``schema_version``, and the manifest pins the ``sha256`` of the exact bytes
that version was published with.  Editing a schema without regenerating the
manifest makes ``validate_contracts.py`` fail with "fingerprint mismatch" --
that is the intended alarm, not a bug.  This script is the sanctioned way to
re-lock after an *intentional* schema change.

Usage::

    python scripts/update_manifest.py          # rewrite the manifest
    python scripts/update_manifest.py --check  # exit 1 when stale (CI)

Only ``schemas[]`` entries and ``generator`` are rewritten; the compatibility
policy and package metadata are preserved verbatim.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = REPO_ROOT / "contracts" / "v1"
MANIFEST_PATH = REPO_ROOT / "contracts" / "manifest.json"

GENERATOR = "scripts/update_manifest.py"
ALGORITHM = "sha256(canonical file bytes)"


def fingerprint(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def render(manifest: dict, *, generated_at: str) -> str:
    """Render the manifest in the layout the repository already uses.

    Schema entries stay one-per-line so that a single hash change produces a
    single-line diff instead of re-flowing the whole file.
    """
    lines = [
        "{",
        f'  "package": {json.dumps(manifest["package"], ensure_ascii=False)},',
        f'  "package_version": {json.dumps(manifest["package_version"], ensure_ascii=False)},',
        '  "schemas": [',
    ]
    entries = []
    for entry in manifest["schemas"]:
        entries.append(
            "    {"
            f'"name": {json.dumps(entry["name"], ensure_ascii=False)}, '
            f'"version": {json.dumps(entry["version"], ensure_ascii=False)}, '
            f'"sha256": {json.dumps(entry["sha256"], ensure_ascii=False)}'
            "}"
        )
    lines.append(",\n".join(entries))
    lines.append("  ],")
    lines.append('  "compatibility_policy": {')
    policy = manifest["compatibility_policy"]
    policy_lines = [f'    {json.dumps(key)}: {json.dumps(value, ensure_ascii=False)}' for key, value in policy.items()]
    lines.append(",\n".join(policy_lines))
    lines.append("  },")
    lines.append(
        '  "generator": {'
        f'"name": {json.dumps(GENERATOR)}, '
        f'"algorithm": {json.dumps(ALGORITHM)}, '
        f'"generated_at": {json.dumps(generated_at)}'
        "}"
    )
    lines.append("}")
    return "\n".join(lines) + "\n"


def refresh(manifest: dict, *, generated_at: str) -> dict:
    """Recompute version + sha256 for every schema currently in contracts/v1.

    The manifest **order** is preserved from the existing file so that a hash
    change touches exactly one line instead of re-sorting the whole list.
    Schemas that disappeared are dropped, and schemas added since the last
    lock are appended in name order so the output stays deterministic.
    """
    refreshed = json.loads(json.dumps(manifest))
    on_disk = {path.name: path for path in SCHEMA_DIR.glob("*.schema.json")}
    ordered = [entry for entry in manifest["schemas"] if entry.get("name") in on_disk]
    seen = {entry["name"] for entry in ordered}
    ordered.extend({"name": name} for name in sorted(on_disk) if name not in seen)

    refreshed["schemas"] = []
    for entry in ordered:
        path = on_disk[entry["name"]]
        schema = json.loads(path.read_text(encoding="utf-8"))
        refreshed["schemas"].append(
            {
                "name": path.name,
                "version": schema["schema_version"],
                "sha256": fingerprint(path),
            }
        )
    refreshed["generator"] = {
        "name": GENERATOR,
        "algorithm": ALGORITHM,
        "generated_at": generated_at,
    }
    return refreshed


def main(argv: list[str]) -> int:
    check = "--check" in argv
    manifest = load_manifest()
    refreshed = refresh(manifest, generated_at=date.today().isoformat())
    rendered = render(refreshed, generated_at=refreshed["generator"]["generated_at"])
    current = MANIFEST_PATH.read_text(encoding="utf-8")

    if check:
        if rendered != current:
            print("STALE: contracts/manifest.json does not match contracts/v1/*.schema.json")
            print("run: python scripts/update_manifest.py")
            return 1
        print("contracts/manifest.json is up to date")
        return 0

    if rendered == current:
        print("contracts/manifest.json already up to date")
        return 0
    MANIFEST_PATH.write_text(rendered, encoding="utf-8")
    print(f"updated {MANIFEST_PATH.relative_to(REPO_ROOT)} ({len(refreshed['schemas'])} schemas)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
