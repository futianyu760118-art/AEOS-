# M02 EDP 企业数据与证据平台 最新方案

**方案版本：** V7.2.2  
**方案状态：** 当前执行候选，待对应 Owner 与 Gate 签批  
**英文名称：** Enterprise Data & Evidence Platform  
**建议起始日：** 2026-10-19（PMO 签发后生效）

## 一 当前定位

AEOS 的企业事实、事件、结果、证据、审计、指标、价值和 Trace 统一关联平台，任何模块通过契约使用，不直接跨域写库。


## 模块代码与正式名称

| 字段 | 当前冻结候选 |
| --- | --- |
| module_id | M02 |
| system_code | EDP |
| system_name | 企业数据与证据平台 |
| system_name_en | Enterprise Data & Evidence Platform |

## 全系统对象代码约束

- 数据库、Event、内部 API 统一使用 snake_case。
- 对象实体使用 PascalCase；禁止使用 `/` 合并多个实体。
- 结果验证实体统一为 `Verification`，动作统一为 `verify`。
- 每个关键对象只有一个 `fact_owner`，并区分 `record_owner`、`processor`、`consumer`、`verifier`。

## 二 当前目标

建立 Fact/Object → Event → Decision、Action → Result → Verification → Evidence 的可回放闭环，支持业务、Agent 和工程结果的可验证、可审计和可恢复。

## 三 Own 范围

- BusinessObject、Event、Result、Evidence、Audit、Metric、Value、Trace 的通用模型
- 数据域、事实 Owner、来源 Provenance、质量规则、Outbox 和重放
- API/Event/Result/Evidence/Decision、Action Contract 的执行和版本管理
- 租户隔离、数据分级、留存、备份、血缘、审计和证据索引

## 四 Must Not 边界

- 不拥有各业务专业事实和算法结果；专业中心保留事实 Owner
- 不允许 EBMS、Agent 或业务模块直接访问其他域数据库
- 不以日志、页面状态或聊天文本替代 Result/Evidence

## 五 核心对象与事实 Owner

| 对象域 | 定义 | Owner |
| --- | --- | --- |
| BusinessObject | 业务对象和事实状态 | 专业中心 |
| Event | 状态变化、来源、时间、主体、对象 | M02 |
| Result、Metric、Value | 计算结果、指标、价值、版本、口径 | 专业中心/M02 |
| Evidence/Provenance | 文件、截图、测试、审批、来源、哈希 | M02 |
| Decision、Action/Verification | 决策、执行、验证、关闭和学习 | M03/业务中心/M02 |

## 六 接口与协作

- M03：只消费 Result、Metric、Exception、Decision、Action、Evidence
- M13：接收 Agent 运行、工作量、成本、绩效和退出证据
- M14：接收需求、变更、构建、测试、发布、部署、回滚和漏洞证据
- M01/M12：记录授权、扫描、发布、告警和恢复证据

## 七 安全控制

- 数据分级、字段脱敏、租户隔离、传输/存储加密和密钥轮换
- Evidence 只追加或版本化，不允许静默覆盖；删除/留存需要授权和证明
- Outbox、幂等、重试上限、死信和重放保护，防止重复外部副作用
- 敏感数据导出、跨租户查询和 Evidence 分享需要审批和审计

## 八 36 周落地安排

| 周期 | Gate | 当前必须完成 |
| --- | --- | --- |
| W05–W08 | G1 | 完成 Data Ownership、Object ID、Contract Pack、Event/Result/Evidence 版本规则 |
| W09–W16 | G2/G3 | 跑通一条真实业务/研发闭环并形成可回放证据 |
| W17–W28 | G4–G6 | 接入 EBMS、业务中心、M13、M14 和 POMS 候选 |
| W29–W36 | G7/G8 | 完成灾备恢复、数据隔离、DLP、审计和最终证据包 |

## 九 验收标准

- 每个关键对象只有一个事实 Owner，来源和版本可定位
- 关键动作均能关联 Event、Result、Evidence、Trace 和授权决定
- 重复提交、失败重试、重放和恢复测试通过
- 备份可恢复、审计不可静默修改、跨租户查询被阻断

## 十 当前来源与证据状态

| 来源 | 状态 | SHA-256 |
| --- | --- | --- |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/EDP数据库/AEOS 企业数据与证据中台 EDP 迭代版总体方案 V1.0.md | AVAILABLE / HASHED | ABFC2BDC96EBE235B3C2FA6E804740AEE570172163A88CF5546B6DFA0CD2EA65 |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/EDP数据库/EDP 数据与智能中台 × AEOS V7.2 架构与代码核准报告 V1.0.md | AVAILABLE / HASHED | A05F623C994EC57086F9C701040BD3045161993FD8CBA57AF15FC0285AB27FF8 |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/EDP数据库/FDE_A档_场景契约与指标字典.xlsx | AVAILABLE / HASHED | 95771F9E256C2714431635C05665DF5099BD82748AA4353487825A6E72D103B5 |

正式 P0-03/P0-04/P0-05 仍需补齐；本方案以 EDP 候选基线作为实现边界，不把候选契约标记为正式冻结。 对应正式文件仍须按 System Registry V1.3 候选字段登记。

## 十一 执行输入

本方案执行输入固定为：AEOS V7.2.2 当前评审基线、9 个月/36 周计划、M01/M02/M12 安全与证据门禁、M13 Hub 与 M14 NOMI 当前边界、对应模块领域资料和经登记的 GitHub/ChatGPT 证据。
