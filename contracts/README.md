# AEOS contract governance

`contracts/` is the single source of truth for cross-system AEOS contracts. Business repositories consume generated packages from this source; they must not maintain duplicate global schemas.

Contract versions use `MAJOR/MINOR/PATCH`:

- `PATCH` fixes wording or non-semantic defects without changing compatibility.
- `MINOR` adds backward-compatible fields or capabilities.
- `MAJOR` changes or removes required semantics. Destructive or incompatible changes always require a `MAJOR` version.

CI must validate schema compatibility, version changes, examples, and generated package fingerprints before a contract change is accepted. A consumer may reject an incompatible version, but may not silently reinterpret a producer's contract.

The current contract documents in this directory remain the architecture references. The Phase 1 registry and future generated contract packages must link back here rather than copying a second global schema source.
