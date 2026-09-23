# AEOS DEH Contract V1

状态：P0 契约执行草案  
适用：Decision & Execution Hub / meeting-helper 迁移

## 1. Common Envelope

所有对象至少携带：
- tenant_id
- id
- version
- source_system
- created_at
- updated_at
- created_by
- correlation_id
- trace_id

## 2. Goal Link Contract

```yaml
goal_id: string
goal_type: string
parent_goal_id: string|null
owner_id: string
period_start: datetime|null
period_end: datetime|null
target: object|null
status: draft|active|achieved|closed|cancelled
```

DEH 不拥有 Goal 主数据，只保存引用。

## 3. Decision Contract

```yaml
decision_id: string
decision_case_id: string|null
goal_id: string|null
source_type: meeting|event|issue|agent|human|system
source_id: string
object_ref:
  object_type: string
  object_id: string
content: string
reason: string|null
decision_owner_id: string
status: draft|confirmed|superseded|cancelled
decided_at: datetime|null
evidence_refs: array
```

## 4. Action Contract

```yaml
action_id: string
decision_id: string|null
goal_id: string|null
source_type: string
source_id: string
object_ref:
  object_type: string
  object_id: string
owner_id: string
owner_role: string|null
description: string
expected_result: object|null
priority: low|medium|high|critical
status: candidate|pending|confirmed|in_progress|blocked|done|cancelled
start_at: datetime|null
due_at: datetime|null
verification_rule: object|null
escalation_rule: object|null
evidence_required: boolean
```

约束：
- meeting_id 不再是必填字段。
- Action 必须拥有稳定 action_id 与 owner_id。
- done 不等于 verified。

## 5. Result Contract

```yaml
result_id: string
action_id: string
object_ref:
  object_type: string
  object_id: string
expected_result: object|null
actual_result: object
status: submitted|verified|rejected|superseded
submitted_by: string
submitted_at: datetime
verified_by: string|null
verified_at: datetime|null
evidence_refs: array
```

## 6. Evidence Contract

```yaml
evidence_id: string
subject_type: decision|action|result|object
subject_id: string
evidence_type: file|image|record|metric|log|approval|external_ref
source_system: string
source_record_id: string|null
uri: string|null
checksum: string|null
version: string|null
confidence: number|null
submitted_by: string|null
submitted_at: datetime
metadata: object|null
```

## 7. Event Contract

```yaml
event_id: string
event_type: string
occurred_at: datetime
source_system: string
object_ref:
  object_type: string
  object_id: string
correlation_id: string
causation_id: string|null
actor_id: string|null
payload_version: string
payload: object
evidence_refs: array
idempotency_key: string
```

首批标准事件：
- MeetingCreated
- MeetingArchived
- DecisionCreated
- DecisionConfirmed
- ActionCreated
- ActionAssigned
- ActionStarted
- ActionBlocked
- ActionOverdue
- ActionCompleted
- ResultSubmitted
- ResultVerified
- ResultRejected
- EvidenceSubmitted

## 8. Verification Rule

Action 完成流程：
candidate → confirmed → in_progress → done → result_submitted → verified

异常路径：
- blocked
- overdue
- rejected
- cancelled

规则：
- done 仅表示执行者声明完成。
- verified 才表示 AEOS 接受结果。
- verification 必须关联 Result + Evidence 或有明确豁免原因。

## 9. Integration Rules

- 跨域写入：禁止 direct DB write。
- 跨域读取：优先 API / Data Service。
- 状态广播：使用 Event。
- 幂等：所有 create/submit 类写操作必须支持 idempotency_key。
- 审计：重大 Decision、Action、Result、Verify 必须可追溯 actor/source/version。
- 兼容：meeting-helper 迁移期可保留 meeting_id，但只能作为 source_id / legacy_ref。

## 10. Contract Gate

进入 G2 前至少验证：
- Schema validation
- Required fields
- Enum compatibility
- Idempotency
- Event replay
- Permission enforcement
- Evidence traceability
- Result verification
- Audit completeness
