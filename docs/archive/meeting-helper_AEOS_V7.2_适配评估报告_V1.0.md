# meeting-helper 与 AEOS V7.2 适配评估报告 V1.0

- **来源仓库**：`chenqxa/meeting-helper`
- **目标体系**：AEOS V7.2 企业自治操作系统
- **归档日期**：2026-09-23
- **资料性质**：架构适配评估 / 归档基线
- **评估依据**：`README.md`、`docs/system-requirements.md`、`docs/api.md`、`docs/schema.sql`

---

## 1. 结论摘要

`meeting-helper` 不应仅定位为“会议纪要助手”，也不建议归入研发、销售、交付、品质、财经或后勤中的任何单一自治中心。

建议正式纳入 AEOS V7.2 的：

> **AEOS 公共能力层——决策与执行闭环中心（Decision & Execution Hub，简称 DEH）**

其核心职责不是“管理会议”，而是把企业中的：

`事件 / 问题 / 会议 → 决策 → 行动 → 责任人 → 执行 → 结果 → 证据 → 稽核 → 复盘`

形成统一执行闭环。

因此，meeting-helper 适合作为 AEOS “决策执行闭环中心”的第一阶段实现基础。

---

## 2. 当前系统实际能力

仓库当前已明显超出普通会议助手范围，主要具备：

### 2.1 会议与输入
- 会议创建、分类、参会人、组织者
- 文本录入
- 音频录入与 ASR 转写
- AI 生成纪要
- AI 抽取行动项
- 纪要人工编辑、确认、锁定
- Word / PDF 导出
- 版本管理

### 2.2 行动与待办
- 行动项描述
- 责任人 / 提出人
- 截止日期
- 优先级
- 状态
- 持续项
- 待定项
- 阻塞
- 逾期
- 完成
- 进度反馈

### 2.3 执行闭环
- 全部任务 / 我的任务 / 群体任务
- 看板 / 日历
- OA / 企业微信 / IM 推送
- 持续项周期提醒
- 完成通知
- 超期识别
- 行动项台账

### 2.4 证据与评价
- 图片证据
- 附件
- OA 回传
- V / X / 0 稽核
- 周例会 / 月度 / 产销会复盘
- 完成率
- 操作日志

这说明当前系统已经具备 AEOS “Decision → Action → Evidence → Review” 的较强雏形。

---

## 3. 在 AEOS V7.2 中的推荐位置

建议目标结构：

```text
AEOS V7.2
│
├── Identity & Permission
├── Goal Engine
├── Data Foundation
├── Event Bus
│
├── Decision & Execution Hub   ← meeting-helper 演进
│
├── EBMS
│
├── 研发自治中心
├── 销售自治中心
├── 交付自治中心
├── 品控自治中心
├── 财经自治中心
└── 后勤自治中心
```

定位原则：

- **不是后勤中心**
- **不是恒聘通子模块**
- **不是 EBMS 普通页面**
- **不是某一个业务自治中心**
- **是所有自治中心共享的企业级执行闭环公共能力**

---

## 4. 与 EBMS 的边界

### EBMS 负责
“企业现在经营得怎么样？”

主要关注：
- 企业目标
- KPI
- 收入
- 毛利
- 应收
- 交付
- 品质
- 风险
- 经营异常
- 最终结果

### Decision & Execution Hub 负责
“决定之后，事情有没有真正执行？”

核心链路：

```text
Decision
↓
Action
↓
Owner
↓
Deadline
↓
Execution
↓
Evidence
↓
Result
↓
Evaluation
```

因此，EBMS 与 DEH 应为平级协作关系：
- EBMS 偏“观察、经营判断、结果展示”
- DEH 偏“决策落地、执行闭环、证据与稽核”

---

## 5. AEOS 能力匹配矩阵

| AEOS 能力 | meeting-helper 当前情况 | 适配判断 |
|---|---|---|
| Meeting | 已完整实现 | 高 |
| Action | 已完整实现 | 高 |
| Owner | 已实现 | 高 |
| Deadline | 已实现 | 高 |
| Todo | 已实现 | 高 |
| Result | 基础实现 | 中高 |
| Evidence | 已有附件 / 截图 / OA 回传 | 中高 |
| Evaluation | 已有 V/X/0 | 中高 |
| Audit | 已有操作日志 | 中高 |
| Decision | 主要存在于纪要文本中 | 中 |
| Goal | 基本缺失 | 低 |
| Object | 未形成 AEOS 统一对象 | 低 |
| Event | 有内部事件，但无 AEOS 统一契约 | 中低 |
| Skill | 以 Prompt 为主 | 中低 |
| Agent | 尚未形成岗位 Agent | 低 |
| Data Foundation | 仍以自身数据库模型为主 | 中低 |

---

## 6. 当前最大架构问题

### 6.1 Meeting 被当成最高业务对象

当前核心关系基本为：

```text
Meeting
   ↓
Action
```

并且行动项主要依赖 `meeting_id`。

这适合会议管理系统，但不适合 AEOS。

企业大量行动并非会议产生，例如：
- 订单逾期
- 客户投诉
- 品质异常
- 库存不足
- 毛利率异常
- 设备故障
- 应收超期
- 供应商延期
- AI Agent 发现风险

这些都应可以直接触发 Decision / Action。

### 6.2 AEOS 推荐模式

```text
Goal
 ↓
Business Object
 ↓
Event / Issue
 ↓
Decision
 ↓
Action
 ↓
Result
 ↓
Evidence
 ↓
Evaluation
```

Meeting 应降级为 Decision 的一种来源，而不是所有 Action 的父对象。

---

## 7. 必须新增的六类 AEOS 核心契约

### 7.1 Goal

建议核心字段：

```text
goal_id
goal_type
parent_goal_id
owner
target_value
current_value
period
status
```

作用：让每个重大行动都能回答“为什么做”。

### 7.2 Decision

建议建立独立 Decision 实体：

```text
decision_id
source_type
source_id
goal_id
object_type
object_id
content
reason
decision_owner
decided_at
status
```

来源可包括：
- meeting
- event
- issue
- agent
- manager
- employee
- system

### 7.3 Action

现有行动项升级为统一 AEOS Action：

```text
action_id
decision_id
goal_id
source_type
source_id
object_type
object_id
owner_id
owner_role
action
expected_result
start_at
due_at
status
priority
risk_level
```

关键要求：

> Action 不再强制依赖 meeting_id。

### 7.4 Result

AEOS 不应只判断“做没做”，还要判断“结果是否达到预期”。

```text
result_id
action_id
expected_result
actual_result
result_type
result_value
completed_at
submitted_by
status
```

从 Task Done 升级为 Result Achieved。

### 7.5 Evidence

建议建立一级 Evidence 对象：

```text
evidence_id
object_type
object_id
action_id
result_id
evidence_type
file_url
source_system
source_record_id
submitted_by
submitted_at
hash
```

证据来源可包括：
- 图片
- 视频
- PDF
- Excel
- ERP
- MES
- 订单
- 付款记录
- 质检报告
- 设备数据
- 人工确认

### 7.6 Event

建议建立统一 AEOS Event Contract。

基础执行事件：
- MeetingCreated
- MeetingArchived
- DecisionCreated
- DecisionUpdated
- ActionCreated
- ActionAssigned
- ActionAccepted
- ActionStarted
- ActionBlocked
- ActionOverdue
- ActionCompleted
- EvidenceSubmitted
- ResultSubmitted
- ResultVerified
- ResultRejected

业务事件示例：
- OrderCreated
- OrderDelayed
- QualityIssueCreated
- CustomerComplaintCreated
- PaymentOverdue
- InventoryShortage
- SupplierDelayed

---

## 8. 与 Data Foundation 的关系

推荐闭环：

```text
业务系统
 ↓
Data Foundation
 ↓
Business Object
 ↓
Event
 ↓
Decision & Execution Hub
 ↓
Action
 ↓
Result
 ↓
Evidence
 ↓
Data Foundation
 ↓
EBMS
```

最终形成：

```text
数据 → 判断 → 决策 → 行动 → 结果 → 数据
```

这应成为 AEOS 自治运行的核心循环。

---

## 9. Agent / Skill 演进建议

### Meeting Agent
- 转写
- 总结
- 决策识别
- 问题识别
- 行动识别
- 风险识别

### Decision Agent
- 决策结构化
- 决策依据整理
- Goal / Object 绑定
- 影响范围识别

### Action Agent
- 行动分类
- 责任人匹配
- 节点判断
- 逾期监控
- 提醒
- 升级

### Evidence Agent
- 证据检查
- 完整性检查
- 来源校验
- 结果关联

### Review Agent
- 结果验证
- 异常判断
- 重复问题识别
- 经验沉淀

原则：先形成稳定契约，再 Agent 化，避免系统过重。

---

## 10. 权限模型调整建议

当前系统主要为：

```text
admin
manager
secretary
employee
```

更接近传统 OA 管理模式。

AEOS 推荐逐步映射为：

```text
Decision Maker
Executor
Observer
System Agent
Admin
```

其中：
- Admin 属于技术权限
- 企业组织角色重点围绕“决策者 / 执行者”
- System Agent 作为数字执行角色参与自动处理

---

## 11. 不建议推倒重做

现有仓库已经积累：
- Meeting
- ASR
- AI Summary
- Action
- Todo
- Push
- OA
- 企业微信
- IM
- Evidence
- Review
- Audit
- Dashboard
- Export
- Project 基础能力

建议路线：

> **保留现有功能 + 抽离公共对象 + 增加 AEOS 契约**

不建议重新做一套会议系统。

---

## 12. 整改优先级

### P0 — 架构门禁

优先完成：

1. 建立 Decision 对象
2. Action 与 Meeting 解耦
3. 增加 Goal ID
4. 建立 Result
5. 建立独立 Evidence
6. 定义 AEOS Event Contract

这是进入 AEOS 的最低架构门槛。

### P1 — 平台接入

接入：
- AEOS SSO
- 组织与权限
- Data Foundation
- Event Bus
- EBMS

### P2 — 业务自治中心接入

建议逐步接入：
1. 品控自治中心
2. 交付自治中心
3. 销售自治中心
4. 研发自治中心
5. 财经自治中心
6. 后勤自治中心

各业务中心只负责产生自己的 Business Object / Event。

DEH 统一负责：

```text
Decision → Action → Result → Evidence
```

### P3 — Agent 化

再建设：
- Meeting Agent
- Decision Agent
- Action Agent
- Evidence Agent
- Review Agent

---

## 13. 推荐产品命名

### 中文
**AEOS 决策与执行闭环中心**

### 英文
**AEOS Decision & Execution Hub**

### 简称
**DEH**

现有“会议纪要与行动项助手”建议保留为 DEH 下的 Meeting Module。

---

## 14. 推荐模块结构

```text
AEOS Decision & Execution Hub
│
├── 01 Goal Link
├── 02 Event Inbox
├── 03 Meeting
├── 04 Decision
├── 05 Action
├── 06 Todo
├── 07 Result
├── 08 Evidence
├── 09 Evaluation
├── 10 Review
├── 11 Notification
├── 12 Audit
└── 13 Agent / Skills
```

---

## 15. 最终结论

`chenqxa/meeting-helper` 已具备较好的企业执行闭环基础。

当前主要问题不是会议功能不足，而是架构仍然“以 Meeting 为中心”。

AEOS V7.2 应将其升级为：

> **以 Goal / Object / Event / Decision / Action / Result / Evidence 为中心的公共执行基础设施。**

建议演进路线：

```text
meeting-helper
↓
Action Execution System
↓
Decision & Execution Hub
↓
AEOS 公共执行基础设施
```

**最终归档判断：建议纳入 AEOS V7.2，并列为公共核心能力模块。**

---

## 16. 后续动作基线

下一阶段首先执行以下六项，不继续优先堆叠会议功能：

- [ ] 建立 AEOS Decision Object
- [ ] Action 与 Meeting 解耦
- [ ] Action 增加 Goal / Business Object 关联
- [ ] 建立 Result Object
- [ ] 建立独立 Evidence Object
- [ ] 建立统一 AEOS Event Contract

完成后再进入 P1 平台接入与 P2 自治中心集成。
