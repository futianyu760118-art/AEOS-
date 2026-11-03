"""人员状态同步合同的本地检查，不连接生产系统。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENT_SCHEMA = ROOT / "contracts" / "v1" / "person-lifecycle-event-v1.schema.json"
RESULT_SCHEMA = ROOT / "contracts" / "v1" / "person-lifecycle-result-v1.schema.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_person_lifecycle_contracts_exist_and_have_versions() -> None:
    for path in (EVENT_SCHEMA, RESULT_SCHEMA):
        document = _load(path)
        assert document["$schema"].endswith("/schema")
        assert document["title"]
        assert document["type"] == "object"


def test_event_contract_allows_only_supported_actions() -> None:
    document = _load(EVENT_SCHEMA)
    actions = document["properties"]["event_type"]["enum"]
    assert set(actions) == {"person.offboarded", "person.reinstated"}
    required = set(document["required"])
    assert {
        "event_id",
        "tenant_id",
        "person",
        "revision",
        "occurred_at",
        "effective_at",
        "correlation_id",
        "trace_id",
        "idempotency_key",
    } <= required


def test_result_contract_exposes_plain_status_and_pending_confirmation() -> None:
    document = _load(RESULT_SCHEMA)
    properties = document["properties"]
    assert {"status", "changed", "received_at"} <= properties.keys()
    assert set(properties["status"]["enum"]) == {
        "synced",
        "skipped",
        "pending_confirmation",
        "retrying",
        "failed",
    }

