# M05 CRM 销售自治中心 最新方案

**方案版本：** V7.2.2  
**方案状态：** 当前执行候选，待对应 Owner 与 Gate 签批  
**英文名称：** Sales Autonomous Center  
**建议起始日：** 2026-10-19（PMO 签发后生效）

## 一 当前定位

销售专业事实和全生命周期自治中心，覆盖 Lead、Customer、Contact、Opportunity、Inquiry、Quotation、Commercial Order 和 Customer Operation。


## 模块代码与正式名称

| 字段 | 当前冻结候选 |
| --- | --- |
| module_id | M05 |
| system_code | CRM |
| system_name | 销售自治中心 |
| system_name_en | Sales Autonomous Center |

## 全系统对象代码约束

- 数据库、Event、内部 API 统一使用 snake_case。
- 对象实体使用 PascalCase；禁止使用 `/` 合并多个实体。
- 结果验证实体统一为 `Verification`，动作统一为 `verify`。
- 每个关键对象只有一个 `fact_owner`，并区分 `record_owner`、`processor`、`consumer`、`verifier`。

## 二 当前目标

建立从线索、客户、商机、询盘、报价、商务订单到客户运营的销售闭环，使每个销售结果、异常、决策和行动可验证。

## 三 Own 范围

- Lead、Customer、Contact、Opportunity、Inquiry、Quotation、Commercial Order、Sales Activity
- SalesResult、SalesException、SalesDecisionRef、SalesEvidenceRef 和 SalesEvent
- 销售 Domain Agent、销售 Skill、销售业务上下文和专业验收
- 产品销售视图、销售材料引用、客户经营和销售风险

## 四 Must Not 边界

- 不拥有 Person/Org/Position、Product/BOM/Certification、Delivery/Capacity、Quality、Revenue/Margin/AR/AP 等专业事实
- 不把 M10 Personal Agent 当成 CRM 主数据 Owner
- 报价、发信、订单和高风险客户动作不得无确认自动执行

## 五 核心对象与事实 Owner

| 对象域 | 定义 | Owner |
| --- | --- | --- |
| Lead/Customer/Contact | 客户、线索、联系人、来源和证据 | M05 |
| Opportunity/Inquiry | 商机、询盘、阶段、需求、匹配和风险 | M05 |
| Quotation/CommercialOrder | 报价、审批、商务订单和状态 | M05 |
| SalesActivity/Result | 沟通、跟进、销售结果和价值 | M05/M02 |
| SalesException/Decision | 价格、信用、交期、合规和客户风险 | M05/M03/M09/M06 |

## 六 接口与协作

- M10：提供 Personal Agent 的销售上下文、Todo、Exception、Past Result 和交互入口
- M04：读取产品销售视图；正式 Product/BOM/Certification 仍由 M04 负责
- M06/M08/M09：引用交付、质量、收入、信用、AR/AP 结果
- M13/M02：接入 Sales Agent Workforce、结果、证据和成本

## 七 安全控制

- 客户、价格、报价、合同、信用和外贸数据按租户、岗位和客户范围隔离
- 公开来源线索必须保留来源证据、去重、验证和人工复核
- 报价、发信、订单、价格和外部写入采用 Guard、人审和审计
- 禁止将客户资料、合同和敏感信息直接送入未授权模型或工具

## 八 36 周落地安排

| 周期 | Gate | 当前必须完成 |
| --- | --- | --- |
| W21–W24 | G5 | 打通销售 Agent、Inquiry/Quote/Follow-up、Result/Evidence 闭环 |
| W25–W28 | G6 | 接入 M10 Personal Agent、M13 Workforce、M03 经营工作面 |
| W29–W32 | G7 | 完成客户隔离、Prompt Injection、发信/报价工具滥用和数据外发测试 |
| W33–W36 | G8 | 完成销售 KPI、复制模板、培训和运营移交 |

## 九 验收标准

- 询盘到报价准备、Guard、人审、发送、跟进、Result、Verification、Evidence 可闭环
- CRM 主数据和销售专业结果由 M05 负责，M10 只提供个人工作面
- 客户、价格、合同和外部沟通权限测试通过
- 销售 Agent 质量、时效、成本和人工验收口径明确

## 十 当前来源与证据状态

| 来源 | 状态 | SHA-256 |
| --- | --- | --- |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/销售自治中心/AEOS_销售全生命周期自治简版方案_V1.2.md | AVAILABLE / HASHED | 0D51324DB841693D99828E2B7FB82729435AF954B8143A340F4430DD137566DF |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/销售自治中心/AEOS_M05_M10_Agent_标准与总体方案_归档资料包_2026-10-10/AEOS_M05_M10_Agent_总体方案_V2.0.md | AVAILABLE / HASHED | B52812BDFBEACB922E63D5EACC12AAE04883BEEC54050985CF11CDAD8D101DDB |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/销售自治中心/AEOS_M05_M10_Agent_标准与总体方案_归档资料包_2026-10-10/M05_M10_边界规范_V1.0.md | AVAILABLE / HASHED | EF33BC0A8ABB3777395F4CB0FCA18E022C083133E3D2FB6146B6B6E35C17A6DD |

M05/M10 当前方案为 G0 待审候选；POMS V2.2 需补齐具体原件后才能转为正式依赖。 对应正式文件仍须按 System Registry V1.3 候选字段登记。

## 十一 执行输入

本方案执行输入固定为：AEOS V7.2.2 当前评审基线、9 个月/36 周计划、M01/M02/M12 安全与证据门禁、M13 Hub 与 M14 NOMI 当前边界、对应模块领域资料和经登记的 GitHub/ChatGPT 证据。
