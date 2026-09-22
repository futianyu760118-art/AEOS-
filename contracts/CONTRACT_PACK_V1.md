# Contract Pack V1

状态：P0 契约骨架。正式 Schema/API 定义由 Architecture Board 批准。

## 1. Object Contract

统一字段至少包括：

- tenant_id
- object_type
- object_id
- source_system
- revision

## 2. API Contract

要求：版本化、认证/授权、输入输出 Schema、错误码、幂等语义、审计字段、Owner。

## 3. Event Contract

要求：event_id、event_type、object_ref、occurred_at、source_system、correlation_id、version、evidence_refs。跨域集成优先通过 Event/Facade，禁止新增 direct import/跨域写表。

## 4. Result Contract

各专业中心以标准 Result 向 EBMS 输出；EBMS 不直接拼专业内部表。Result 必须支持 source/version/evidence_refs，并能被验证。

## 5. Evidence Contract

关键结果、Decision、Action 必须可追溯到 source/version/checksum/confidence，支持从管理结果穿透到原始记录。

## 6. Decision / Action Contract

链路统一为：

Fact → Event → DecisionCase → Decision → Action → Result → Verify → Evidence

Action 必须具有 Owner、Deadline、状态、Verification 和回滚/升级路径。

## Contract Gate

Contract Test 未通过，不得作为 G2 平台门禁的正式能力。
