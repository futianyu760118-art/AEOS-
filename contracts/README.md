# AEOS contract governance

`contracts/` is the single source of truth for cross-system AEOS contracts. Business repositories consume generated packages from this source; they must not maintain duplicate global schemas.

Contract versions use `MAJOR/MINOR/PATCH`:

- `PATCH` fixes wording or non-semantic defects without changing compatibility.
- `MINOR` adds backward-compatible fields or capabilities.
- `MAJOR` changes or removes required semantics. Destructive or incompatible changes always require a `MAJOR` version.

CI must validate schema compatibility, version changes, examples, and generated package fingerprints before a contract change is accepted. A consumer may reject an incompatible version, but may not silently reinterpret a producer's contract.

The current contract documents in this directory remain the architecture references. The Phase 1 registry and generated packages link back here rather than copying a second global schema source.

## Versioned source package

`contracts/v1/` is the generated-package source. Consumers must use the exact
schema bytes listed in `contracts/manifest.json`; do not hand-edit a generated
consumer copy. A package is generated only from these versioned schemas, and
the manifest SHA-256 values must be regenerated in the same change.

Compatibility follows semantic versions: MAJOR changes required semantics or
removes fields and requires a migration window; MINOR adds backward-compatible
optional fields or capabilities; PATCH fixes non-semantic defects without
changing compatibility. Run `python scripts/validate_contracts.py` from the
repository root to validate the package and its fingerprints; after changing a
schema, regenerate the manifest fingerprints with:

```text
python -c "import hashlib, pathlib; [print(p.name, hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(pathlib.Path('contracts/v1').glob('*.schema.json'))]"
```
