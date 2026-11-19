# ADR-2026-003: business-event-v1 保持冻结，V2 信封由出站边界投影

- Status: Accepted
- Owner: owner.m05（CRM）+ owner.m02（EDP 消费端）
- Effective Date: 2026-11-18
- Supersedes: —

## Context

中央契约 `contracts/v1/business-event-v1.schema.json`（schema_version 1.0.1）是十二个系统
共用的事件形状，`additionalProperties: false`，必填 12 项：

```
tenant_id, event_id, event_type, source_system, object_type, object_id,
revision, occurred_at, trace_id, idempotency_key, owner_system, payload
```

M05（CRM）在 2026-11 的 PAND-330 里引入了 `AEOS.Event.V2` 独立信封（`backend/app/contracts/aeos.py`），
形状与中央 schema 不同：

| 差异 | BusinessEventV1 | AEOS.Event.V2 |
| --- | --- | --- |
| 对象标识 | 扁平 `object_type` + `object_id` | 嵌套 `object_ref{object_type, object_id}` |
| 租户 | 必填 `tenant_id` | 无（隐含在连接租户） |
| 修订号 | 必填 `revision`（最小 1） | 无（在 payload 内） |
| 链路 | `trace_id` 必填、`correlation_id` 可选 | `correlation_id` 必填、`trace_id` 可选 |
| 归属 | 必填 `owner_system` | 由 `source_system` 承担 |

V2 之所以存在，是因为 L2 事件需要 `actor_id` / `payload_version` / `causation_id` / `evidence_refs`
这些 L1 没有的字段，而 L1 的严格消费端（EBMS 的旧摄入路径）不接受额外字段。两条需求同时成立，
所以出现了"同一系统两种信封"。

问题在于：如果不裁决，`contracts/` 与 `CRM` 会各自演进，最终没有任何一个系统能说清
"AEOS 事件长什么样"——这正是 2026-11-06 审计里"契约三源"的成因。

## Decision

1. **中央 schema 冻结在 1.0.1**：不为 M05 一家改形状。`additionalProperties: false` 与必填 12 项不变，
   版本号不动，manifest 指纹已按 ADR-2026-001 重新上锁。
2. **V2 是 M05 的系统内信封，不是中央契约**：V2 只用于 M05 → 已适配 V2 的消费端（当前为 EBMS 的
   L2 Result 通道），不进入 `contracts/`。
3. **跨形状由出站边界投影解决**：M05 提供纯函数
   `backend/app/contracts/projection.py::project_business_event_v1`，把 V2 投影成 BusinessEventV1
   （`object_ref` 摊平、`tenant_id`/`revision` 从信封或 payload 回退、`trace_id` 由 `correlation_id` 兜底、
   `owner_system` 恒 M05、空证据不输出）。投影**不做业务加工**，只做形状转换。
4. **默认行为不变**：`EBMS_EVENT_ENVELOPE=v2`（默认）时投递原样；置为 `v1` 才投影。切换是配置级
   而非代码级，便于按消费端能力灰度。
5. **幂等键在投影之前计算**：换信封形状不得改变幂等键，否则与 enqueue 时的 `integration_log`
   对不上，会对同一事件重复投递。
6. **投影失败即死信**：缺必填字段属确定性错误，重试无意义（与 `ContractValidationError` 同处理）。
7. 跨仓一致性以测试固化：设 `AEOS_CONTRACTS_DIR` 指向本仓库 `contracts/v1` 时，
   `backend/tests/test_event_projection.py` 会读真实 schema 校验"必填齐全 + 无 schema 外键"；
   未设置则跳过，保证 CRM 在无 AEOS 检出的机器上仍可跑测试。

## Alternatives

- **A. 把 central schema 升到 1.1.0，接受 `object_ref`**：需要十二个系统同时兼容两种形状，
  且 `additionalProperties: false` 下表达"二选一"要引入 `oneOf`，校验错误信息会变差；
  为单一系统的便利改共用契约，等于承认"最新系统定义标准"。
- **B. 让 CRM 只在内部用 V2、外部一律改回 V1**：会丢掉 `actor_id`/`payload_version`/`causation_id`，
  L2 证据链断裂；且 EBMS 的 V2 通道已经上线，回退是重写而非重构。
- **C. 让每个消费端自己写映射**：就是当前"契约三源"的现状，已证明不可维护。

## Consequences

- 正向：中央契约保持单一形状，新系统只需实现一份投影（或直接消费 V1）；M05 的 L2 能力不被削平。
- 正向：投影是纯函数且有 schema 级测试，形状漂移会在 CI 里红，而不是等到联调。
- 负向：M05 出站多一次拷贝；`v1` 模式下 `payload` 内的 `revision` 与顶层 `revision` 可能不一致，
  以 payload 为准（已在函数内注释）。
- 负向：投影函数属于 M05 代码，EDP 若要消费 V1 事件，需自行实现同一投影或等待 `contracts/`
  提供参考实现——本 ADR 只冻结"不改中央 schema"这一条。

## Rollback

`EBMS_EVENT_ENVELOPE` 置回 `v2` 即可恢复原投递形状；`projection.py` 与测试可整体 revert，
不影响 `aeos.py` 的 V2 定义。

## Evidence

- CRM：`python -m pytest -q` → 340 passed, 73 skipped（投影用例 13 个，含 schema 一致性）
- CRM：`AEOS_CONTRACTS_DIR=<AEOS>/contracts/v1 python -m pytest tests/test_event_projection.py -q` → 13 passed
- AEOS：`python scripts/validate_contracts.py` → passed；`python scripts/validate_registry.py` → passed
- 投影输出与 `business-event-v1.schema.json` 的 `required` 集合逐项相等，且无 schema 外键
