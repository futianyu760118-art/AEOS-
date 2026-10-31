# AEOS Decision & Execution Hub（DEH）边界定义 V1

状态：P0 架构执行草案  
上位基线：AEOS V7.2 / System Registry V1  
来源：meeting-helper 适配评估

## 1. 定位

DEH（Decision & Execution Hub，决策与执行闭环中心）是 AEOS 的**跨模块逻辑执行枢纽**，不是新的一级系统编号。

其能力归属：
- M01 AEOS Kernel：Goal / DecisionCase / Decision / Action / Task / Permission / Guard
- M02 Enterprise Data & Evidence Platform：Business Object / Event / Evidence / Audit / Provenance
- M03 EBMS：消费 Result / Exception / Decision / Evidence，不承载专业执行逻辑
- M04~M09：产生专业 Business Object、Event、Result，调用 DEH 形成执行闭环
- M10 POMS：向执行者呈现 Todo、Action、Evidence 提交与反馈入口
- M11：提供 API Gateway / Connector / Event Bus
- M12：提供 Contract Test / Audit / Observability / Release Gate

因此 DEH 是一条运行链，而不是打破 System Registry 的新一级模块。

## 2. 目标运行链

Fact → Event → DecisionCase → Decision → Action → Result → Verify → Evidence

其中 Meeting 仅是 Event / Decision 的一种来源，不再是 Action 的强制父对象。

## 3. meeting-helper 目标归属

现有 meeting-helper 保留以下能力：
- Meeting / Transcript / ASR
- AI Summary / Action extraction
- Todo / Kanban / Calendar
- OA / WeCom / IM Notification
- Continuous Action
- Evidence Upload
- Verification / V-X-0
- Weekly / Monthly Review
- Audit / Export

演进目标：
1. Meeting 降级为 source_type=meeting 的来源对象。
2. Action 与 meeting_id 解耦。
3. 增加 Goal / Business Object / Decision 关联。
4. Result 独立建模。
5. Evidence 独立建模并由 M02 托管标准。
6. 所有跨域变化通过 Event / API Contract 交换。
7. DEH 只编排执行，不持有各专业中心的业务主数据。

## 4. 模块边界红线

- 不新增 M13 或新的一级系统编号。
- 不把 DEH 做成超级 OA / 超级项目管理系统。
- 不允许 DEH 直接跨域写 M04~M09 的专业数据库。
- 不允许 EBMS 直接写 Action / Evidence 内部表。
- 不允许 Meeting 成为所有 Action 的必填父对象。
- 不允许 LLM 绕过 Guard 直接完成重大 Decision 或 Result Verify。
- Evidence 必须保留 source/version/checksum/provenance。
- Contract Test 未通过不得进入正式集成。

## 5. 责任划分

| 能力 | Owner |
|---|---|
| Goal / Decision / Action 语义 | M01 |
| Object / Event / Evidence / Provenance | M02 |
| Result 管理视图 | M03 |
| 专业事实与专业 Result | M04~M09 |
| 个人 Todo / Feedback | M10 |
| Event Bus / Connector | M11 |
| Contract Test / Release Gate | M12 |

## 6. 最小接入条件

任一业务中心接入 DEH 前必须满足：
- 可提供稳定 object_ref
- 可发布标准 Event
- Action 不直接写回专业表
- Result 有明确验收标准
- Evidence 可追溯
- 具备幂等键与 correlation_id
- 具备权限与审计信息

## 7. 第一阶段范围

第一阶段只冻结契约，不重写 meeting-helper：
- Goal Link
- Decision
- Action
- Result
- Evidence
- Event

后续源码迁移必须基于本边界执行。


## 8. Professional Operation Surface（AEOS V7.2.2 增补）

DEH 只负责跨模块逻辑执行闭环，不替代专业自治系统操作界面。

统一原则：
- M04～M09 及后续专业自治系统必须拥有各自正式专业操作面；
- M10 POMS 负责 Todo / Action / Feedback / Deep Link，不复制完整专业业务逻辑；
- M03 EBMS 负责 Result / Exception / Decision / Evidence，不承担专业录入和审批主界面；
- 专业状态变化必须由 Domain Owner System 执行；
- POMS / EBMS / Agent 发起专业动作时，必须经过 SSO Deep Link 或标准受控 API；
- Agent 不得绕过 Domain Operation Surface 与 M01 Guard 直接写最终状态。

受控原则文件：`architecture/PROFESSIONAL_OPERATION_SURFACE_V1.md`。
