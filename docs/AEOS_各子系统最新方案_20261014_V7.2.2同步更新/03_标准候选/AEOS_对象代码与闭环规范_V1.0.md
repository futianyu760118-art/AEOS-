# AEOS 对象代码与闭环规范 V1.0

**状态：** CANDIDATE / G1 前置  
**适用范围：** API、数据库、Event Envelope、Result、Evidence、Decision、Action、Verification 和跨模块 Adapter

## 一 ID 命名

| field_name | 语义 | 事实 Owner | 使用要求 |
| --- | --- | --- | --- |
| tenant_id | 租户 | M01 | 所有跨租户对象和事件的隔离边界 |
| system_id | 系统 | M00 | System Registry 的系统唯一标识 |
| object_id | 对象 | M02 | Object/BusinessObject 的通用唯一标识 |
| event_id | 事件 | M02 | 状态变化、来源、主体和时间 |
| goal_id | 目标 | M03/业务中心 | 目标和指标关联 |
| decision_id | 决策 | M03/业务中心 | 决策案例和审批关联 |
| action_id | 行动 | 专业中心/M03/M14 | 行动、执行、回执和升级关联 |
| result_id | 结果 | 专业中心/M02 | 可验证业务或工程结果 |
| verification_id | 验证 | 专业中心/M02 | 验证动作和验证结论 |
| evidence_id | 证据 | M02 | 文件、测试、审批、回执、来源和哈希 |
| trace_id | 链路 | M02/M12 | 跨服务、跨模块和跨 Agent 追踪 |
| person_id | 人员 | M01 | 人员身份引用 |
| org_id | 组织 | M01 | 组织身份引用 |
| position_id | 岗位 | M01 | 岗位身份引用 |
| agent_id | 智能体 | M01/M13 | Agent 身份引用 |
| team_id | 团队 | M01/M13 | 组织或 Agent Team 引用 |
| task_id | 任务 | 专业中心/M14 | 业务任务或工程任务 |

统一要求：

- 数据库、Event、内部 API 统一使用 snake_case。
- React/TypeScript ViewModel 可以使用 camelCase，但必须经过 Adapter 转换。
- 禁止在同一契约中混用 `objectId`、`object_id`、`ObjectID`。

## 二 Owner 字段

| field_name | 中文 | 定义 | 责任 |
| --- | --- | --- | --- |
| fact_owner | 事实 Owner | 对一个关键 Object/Result 只能有一个 | 负责事实定义、专业结果和最终事实责任 |
| record_owner | 记录 Owner | 通常为 M02 或产生记录的域 | 负责记录、证据、审计和留存 |
| processor | 处理者 | 执行计算、转换或动作的服务/Agent/人员 | 不自动获得事实 Owner 权限 |
| consumer | 消费者 | 读取或引用结果的模块 | 只能按契约消费，不复制事实 |
| verifier | 验证者 | 负责验证结果的人或岗位 | 对 Verification 结论负责 |

每个关键 Object/Result 必须有且只有一个 `fact_owner`；`record_owner`、`processor`、`consumer`、`verifier` 可以同时存在，但不得替代事实 Owner。

## 三 AEOS 核心闭环

```text
Object
  ↓
Event
  ↓
Exception       optional
  ↓
Decision        optional
  ↓
Action
  ↓
Result
  ↓
Verification
  ↓
Evidence
  ↓
Value
  ↓
Learning
```

`Fact` 是 Object 当前被验证的事实状态，不是独立流程节点。

## 四 对象命名

- 对象名称采用 PascalCase，例如 `AgentRegistry`、`DecisionCase`、`TechnicalDebt`。
- 禁止用 `/` 把多个对象写成一个 schema、API 或 Event 名称；`Result`、`Metric`、`Value` 必须分别建模。
- 对象实体统一使用 `Verification`；动作统一使用 `verify`。
- 文档中可以用“对象组”表达多个对象，但 schema、数据库、API 和 Event 必须拆分。

## 五 Event Envelope 最低字段

```json
{
  "event_id": "evt_...",
  "tenant_id": "ten_...",
  "system_id": "M02-EDP",
  "object_id": "obj_...",
  "event_type": "object.updated",
  "actor_id": "agent_...",
  "trace_id": "trace_...",
  "occurred_at": "2026-10-15T00:00:00Z",
  "schema_version": "v1",
  "evidence_ids": []
}
```
