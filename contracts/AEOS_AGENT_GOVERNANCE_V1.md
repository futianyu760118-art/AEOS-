# AEOS Agent 分层、装配与治理规范 V1.0

> 日期：2026-10-10  
> 上位框架：AEOS V7.2  
> 状态：PROPOSED / G0 待审批  
> 适用范围：M01~M12 所有使用 LLM、Agent、Skill、Tool、Memory 的系统与能力

## 1. 目的

统一 AEOS 中 Agent 的分类、装配、权限、运行、审计、评测和回滚规则，防止各自治中心自行建设互不兼容的智能体体系，防止 Agent 数量失控、权限越界、业务事实归属混乱和不可追责。

## 2. 基本原则

1. Agent 是受治理的企业能力，不是自由脚本。
2. 每个人可以有一个 Personal Agent 逻辑实例，但不得“一人一套代码/服务”。
3. 需要推理、规划、多步骤协同的能力才定义为 Agent；确定性能力优先定义为 Skill；单纯访问外部系统定义为 Tool/API。
4. M01 拥有 Agent Runtime / Registry / Skill Registry / Memory Policy / Permission / Guard。
5. M10 负责 Personal Agent 的岗位装配、Personal Context、UI Manifest 与人机交互，不建设第二套 Agent Kernel。
6. M04~M09 拥有专业领域 Agent 的业务语义、业务 Owner、专业 Skill 和专业 Result。
7. Agent 不得成为业务主数据 Owner。
8. Agent 不得绕过 Guard、权限或人工责任链写入重大正式数据。
9. AI 不可用时，业务必须可降级到人工继续运行。
10. 代码完成不等于业务完成；Agent 必须通过 Evaluation + Gate + Evidence 后才能进入生产。

## 3. 分层模型

### 3.1 Personal Agent

面向一个具体人的唯一 AI 入口。

逻辑实例公式：

```
Personal Agent
=
Shared Agent Runtime
+ actor_id
+ positions
+ responsibilities
+ goals
+ permissions
+ business_context
+ personal_context
+ domain_agent_refs
+ guard_policy
+ memory_policy
```

要求：
- Personal Agent 不是独立代码仓、独立模型、独立数据库。
- 同一人员兼岗时按 role_context / responsibility_context 装配。
- 岗位撤销、授权过期、离职后必须刷新或终止实例。
- Personal Agent 不拥有 Customer / Order / Product / Finance 等业务事实。

### 3.2 Domain Agent

由专业自治中心拥有的公共专业智能体，例如：
- sales.inquiry
- sales.quotation
- rd.requirement_analysis
- quality.capa
- finance.credit
- delivery.promise

Domain Agent 必须指定 Business Owner 和 Domain Owner。

### 3.3 Sub-Agent

仅在以下条件满足时允许定义：
- 任务本身需要独立推理或规划；
- 有独立输入输出 Contract；
- 有独立 Owner / KPI / Guard；
- 不能用一个确定性 Skill 替代。

禁止把每一个查询、计算、格式化、校验动作都拆成 Agent。

### 3.4 Skill

确定性或弱自治的可复用专业能力，例如：
- product_match
- calculate_discount
- customer_health_check
- inquiry_classify
- evidence_collect
- result_verify_assist

Skill 必须版本化：`skill_id@version`。

### 3.5 Tool / API

单纯读取或执行系统能力，例如：
- GET Customer
- POST Quote Draft
- Search Product
- Publish Event

Tool 不承载业务责任，不拥有 Memory。

## 4. Agent Registry 最小字段

每个 Agent 必须登记：

```yaml
agent_id: sales.inquiry
agent_type: domain
version: 1.0.0
business_owner: M05
technical_owner: AEOS-AI-Team
runtime_owner: M01
allowed_objects:
  - Lead
  - Customer
  - Inquiry
allowed_actions:
  - analyze
  - classify
  - draft
forbidden_actions:
  - send_external_message
  - approve_quote
  - change_bottom_price
  - promise_delivery
allowed_skills: []
allowed_tools: []
guard_policy_refs: []
memory_policy_ref: ""
model_policy_ref: ""
prompt_version: ""
cost_budget: {}
timeout_seconds: 60
retry_policy: {}
fallback_policy: {}
evaluation_policy_ref: ""
rollback_version: ""
status: draft|approved|active|suspended|retired
```

## 5. Agent / Skill 判定门槛

### 必须定义为 Agent
同时满足至少两项：
- 需要多步骤规划；
- 需要选择不同 Skill；
- 需要上下文推理；
- 需要根据结果动态调整路径；
- 有独立业务结果与责任人。

### 应定义为 Skill
满足以下任一：
- 明确规则计算；
- 固定输入输出转换；
- 查询/匹配/校验；
- 一次性模型抽取但无独立自治目标。

### 应定义为 Tool/API
- 外部系统读写；
- 数据库/服务调用；
- 文件上传；
- 消息投递；
- Event 发布。

## 6. 调用层级与运行限制

默认限制：
- Personal Agent → Domain/Sub-Agent：最大深度 2；
- Domain Agent → Sub-Agent：最大深度 1；
- Sub-Agent 不得继续无限创建新 Agent；
- 单任务 Agent 调用次数必须可配置；
- 必须有 timeout、retry、loop detection、cost budget；
- 超预算或超时进入 fallback / human queue；
- 不允许 Agent 自主注册新 Agent。

## 7. 权限与 Guard

所有正式动作执行前必须重新鉴权，不能仅依赖 UI 是否显示。

至少区分：
- read
- recommend
- draft
- submit
- approve
- verify
- publish
- external_send

重大动作必须 Guard：
- 报价例外；
- 信用/账期；
- 独家授权；
- 交期承诺；
- 认证声明；
- 财务确认；
- 放行；
- 设备控制。

LLM 不得自行决定是否拥有权限。

## 8. Memory 分层

### Enterprise Memory
企业制度、标准、知识。

### Role Memory
岗位方法、Skill、经过批准的经验。

### Business Memory
客户、订单、项目、产品、报价等企业业务事实。归专业中心/M02，不归个人。

### Personal Memory
个人工作偏好、UI偏好、非正式辅助上下文。

红线：
- 客户业务事实不得进入只属于某人的 Personal Memory。
- 人员离职后 Business Memory 保留，Personal Memory 按策略封存/清理。
- Memory 写入必须记录来源、作用域、版本、Owner。

## 9. 身份与审计

所有 Agent 执行链至少记录：
- actor_type
- human_id
- agent_id
- agent_version
- skill_id / skill_version
- model
- prompt_version
- policy_version
- object_ref
- correlation_id
- trace_id
- result_ref
- evidence_refs
- timestamp

必须能回答：谁发起、哪个 Agent、哪个版本、用了什么 Skill、哪条 Policy 放行、结果是什么、证据在哪里。

## 10. Agent Evaluation

M12 统一提供评测与 Gate。

至少评估：
- Accuracy
- Hallucination
- Compliance
- Latency
- Cost
- Human adoption
- Override rate
- Error rate
- Result quality
- Business improvement

每个 Agent 必须定义自己的业务 KPI，不能以“调用次数”作为绩效。

## 11. 自进化规则

禁止生产 Agent 自行修改 Prompt / Skill / Policy 后直接上线。

标准流程：

```
运行数据
→ 生成候选改进
→ Offline Eval
→ Human Review
→ Contract Test
→ Canary
→ Evidence
→ 正式发布
→ 可回滚
```

## 12. 降级与业务连续性

原则：AI unavailable ≠ Business unavailable。

每个 Agent 必须定义：
- fallback rule
- fallback model
- human queue
- degraded UI
- manual SOP

## 13. Gate

### G0
Agent 类型、Owner、边界、数据权限、Guard 已冻结。

### G1
Skill/Tool Contract、输入输出 Schema、权限测试通过。

### G2
Runtime / Registry / Audit / Cost / Timeout / Idempotency 通过。

### G3
至少一条业务闭环达到 Result + Verify + Evidence。

### G4
业务试运行 KPI 达标。

### G5
Agent Evaluation、红队、安全、回滚通过。

### G6
跨企业复制时不复制业务事实、不修改公共内核，价值结果有证据。

## 14. 一级红线

- 禁止一人一套 Agent 代码。
- 禁止 Agent 自主扩大权限。
- 禁止 Agent 直接成为专业主数据 Owner。
- 禁止未登记 Agent 进入生产。
- 禁止未评测 Prompt 自动发布。
- 禁止直接把外部网络信息写成正式企业事实。
- 禁止重大业务动作无 Guard / Owner / Evidence。
