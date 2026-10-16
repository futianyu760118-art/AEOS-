# M09 FAC 财经自治中心 最新方案

**方案版本：** V7.2.2  
**方案状态：** 当前执行候选，待对应 Owner 与 Gate 签批  
**英文名称：** Finance Autonomous Center  
**建议起始日：** 2026-10-19（PMO 签发后生效）

## 一 当前定位

企业经营财经事实、盈利判断、现金判断、预算、成本、风险、财务预测和价值结果的专业自治中心。


## 模块代码与正式名称

| 字段 | 当前冻结候选 |
| --- | --- |
| module_id | M09 |
| system_code | FAC |
| system_name | 财经自治中心 |
| system_name_en | Finance Autonomous Center |

## 全系统对象代码约束

- 数据库、Event、内部 API 统一使用 snake_case。
- 对象实体使用 PascalCase；禁止使用 `/` 合并多个实体。
- 结果验证实体统一为 `Verification`，动作统一为 `verify`。
- 每个关键对象只有一个 `fact_owner`，并区分 `record_owner`、`processor`、`consumer`、`verifier`。

## 二 当前目标

将收入、成本、毛利、应收、应付、现金、预算、投资和 ROI 统一形成 Fact → Event → Decision → Action → Result → Verification → Evidence → Value。

## 三 Own 范围

- 财务对象、成本、收入、毛利、AR/AP、现金、预算、投资和 ROI 专业事实
- 财经计算、版本、口径、预测、风险识别和财经 Result
- 财经 Agent/Skill 的建议、解释、证据和人工验收
- 价值账、成本归集、经营财经异常和审批引用

## 四 Must Not 边界

- 不直接读取 ERP/CRM/SPC/HR/MES 数据库，统一通过 M02 接入
- 不让 Agent 直接付款、改账、改预算或确认财务结论
- 不复制 EBMS 的经营看板和管理行动；M03 只消费财经 Result/Exception/Decision、Action

## 五 核心对象与事实 Owner

| 对象域 | 定义 | Owner |
| --- | --- | --- |
| FinanceFact | 收入、成本、毛利、AR, AP、现金、预算、投资等事实 | M09 |
| FinanceEvent | 交易、结算、收款、付款、成本、预算变化 | M09/M02 |
| FinanceResult | 毛利、现金、预算、ROI、预测、风险结果 | M09 |
| FinanceDecision、Action | 融资、预算、收款、成本和风险行动 | M09/M03 |
| ValueLedger | 价值、成本、收益、口径、周期和证据 | M09/M02 |

## 六 接口与协作

- M02：Source Adapter、Object、Event、Evidence、Provenance、DQ、Value Ledger
- M03：提供 Margin、Cash、AR、ROI、Exception、Decision、Action 和 Evidence
- M05/M06/M07：引用销售、交付、人力、成本和履约结果
- M13/M14：管理财经 Agent 工作和财经系统变更证据

## 七 安全控制

- 财务、薪酬、客户信用、银行和税务数据强隔离、加密和最小权限
- 付款、改账、预算、信用、税务和资金动作采用职责分离和双人审批
- 财务计算必须有版本、输入、口径、公式、时间窗口和 Evidence
- 禁止秘密、银行凭证、税务信息进入 Prompt、日志或未授权外部工具

## 八 36 周落地安排

| 周期 | Gate | 当前必须完成 |
| --- | --- | --- |
| W17–W20 | G4 | 建立 M09 财经 Result 与 M03 经营异常/决策闭环 |
| W25–W28 | G6 | 接入 M13 财经 Agent 绩效/成本和 M14 财经相关系统变更 |
| W29–W32 | G7 | 完成资金、权限、数据导出、供应链和灾备测试 |
| W33–W36 | G8 | 完成财经 KPI、结算/审计证据、运营移交和复制模板 |

## 九 验收标准

- 毛利、现金或 ROI 至少一条 Result Contract 可由输入追溯到 Evidence
- 财务事实和算法由 M09 Owner 负责，EBMS 不复制专业计算
- 付款、改账、预算和信用动作的审批、职责分离和审计通过
- 财务数据备份恢复、导出控制和敏感信息防护通过

## 十 当前来源与证据状态

| 来源 | 状态 | SHA-256 |
| --- | --- | --- |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/FAC财经自制中心/AEOS V7.2 — M09 FAC  V2.1财经自治中心完整总体方案与分阶段实施计划.md | AVAILABLE / HASHED | 2978D87CD4553391A7D07C6B89C46395E048E9A8F025FE015A713176F667F8B6 |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/FAC财经自制中心/AEOS V7.2 — M09 FAC 第一阶段 MVP 开发执行方案 V1.1.md | AVAILABLE / HASHED | 7D4A0F1E13819357DD0F065550B922559C9BC3FB6534D4F9039D38677E49F8C8 |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/FAC财经自制中心/FAC行动计划.md | AVAILABLE / HASHED | FF22EFC94F5235262FC2E0A0C0D806FAE51A01967661BC6FAD2764B9D258DBEB |

FAC V2.1 和 MVP V1.1 作为当前财经领域输入；正式接入仍需 M02 Contract、M01 权限和业务 Owner 验收。 对应正式文件仍须按 System Registry V1.3 候选字段登记。

## 十一 执行输入

本方案执行输入固定为：AEOS V7.2.2 当前评审基线、9 个月/36 周计划、M01/M02/M12 安全与证据门禁、M13 Hub 与 M14 NOMI 当前边界、对应模块领域资料和经登记的 GitHub/ChatGPT 证据。
