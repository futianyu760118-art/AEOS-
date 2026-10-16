# M03 EBMS 企业经营管理系统 最新方案

**方案版本：** V7.2.2  
**方案状态：** 当前执行候选，待对应 Owner 与 Gate 签批  
**英文名称：** Enterprise Business Management System  
**建议起始日：** 2026-10-19（PMO 签发后生效）

## 一 当前定位

AEOS 的经营结果、异常、决策、行动和管理工作面，消费各专业中心的 Result/Evidence，不复制专业主数据和专业算法。


## 模块代码与正式名称

| 字段 | 当前冻结候选 |
| --- | --- |
| module_id | M03 |
| system_code | EBMS |
| system_name | 企业经营管理系统 |
| system_name_en | Enterprise Business Management System |

## 全系统对象代码约束

- 数据库、Event、内部 API 统一使用 snake_case。
- 对象实体使用 PascalCase；禁止使用 `/` 合并多个实体。
- 结果验证实体统一为 `Verification`，动作统一为 `verify`。
- 每个关键对象只有一个 `fact_owner`，并区分 `record_owner`、`processor`、`consumer`、`verifier`。

## 二 当前目标

将经营管理统一为 Result → Exception → Decision → Action → Result → Verification → Evidence，形成可执行、可复盘的经营闭环。

## 三 Own 范围

- 经营目标、经营指标、异常池、决策案例、行动项、升级和经营看板
- 跨专业结果汇总、偏差识别、管理层决策引用和行动督办
- 经营类 Exception、Decision、Action 的生命周期和验收引用
- 经营管理工作面、权限、通知、升级和责任分派

## 四 Must Not 边界

- 不拥有 Sales、Delivery、Finance、Quality、R&D 的专业事实
- 不直接 CRUD 业务域数据库，不复制各专业算法
- AI 只做识别、建议和草案，不直接改变经营事实或执行不可逆动作

## 五 核心对象与事实 Owner

| 对象域 | 定义 | Owner |
| --- | --- | --- |
| ManagementGoal | 企业, 组织, 岗位, 项目目标和指标口径 | M03/业务 Owner |
| Exception | 异常、严重度、原因、证据、责任和期限 | 专业中心/M03 |
| DecisionCase | 待决策事项、选项、影响、依据和审批 | M03 |
| Action | 行动、Owner、期限、状态、结果和验证 | M03/执行中心 |
| ManagementResult | 经营结果、偏差、趋势、价值和证据 | M03/M02 |

## 六 接口与协作

- M02：消费 Result/Metric/Exception/Decision、Action/Evidence
- M04–M11：提交专业结果、异常、行动回执和证据引用
- M13/M14：消费 Agent/工程绩效和交付状态，不接管其事实 Owner

## 七 安全控制

- 经营指标按组织、岗位、租户和敏感级别授权
- 资金、客户、价格、人员和生产影响的行动必须人审
- 管理看板只消费已验证 Result，展示层不能写回事实
- 所有 Decision、Action 必须记录建议来源、审批人、执行人和证据

## 八 36 周落地安排

| 周期 | Gate | 当前必须完成 |
| --- | --- | --- |
| W17–W20 | G4 | 建立经营 Exception/Decision、Action/Result 业务闭环 |
| W21–W28 | G5/G6 | 接入销售、交付、研发、财务和 Agent 绩效结果 |
| W29–W32 | G7 | 开展经营数据隔离、权限、人工审批和异常升级测试 |
| W33–W36 | G8 | 完成经营 KPI、运营移交和管理复制模板 |

## 九 验收标准

- 至少一条经营异常从识别到 Decision、Action、Result、Verification、Evidence 闭环
- EBMS 不直接读专业库、不复制专业算法
- 高风险经营动作有审批、责任人和证据
- 管理指标口径、来源、时间窗口和 Owner 清晰

## 十 当前来源与证据状态

| 来源 | 状态 | SHA-256 |
| --- | --- | --- |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/EBMS企业经营管理/EBMS_AEOS_V7.2_整改实施方案与12周行动计划_V1.0.docx | AVAILABLE / HASHED | CAAD9FB4C62197399CB5BD1B6E0A2F4F796FABED954D3A494759566DE3880AB0 |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/EBMS企业经营管理/EBMS_AEOS_V7.2_核对评估报告_V1.0.docx | AVAILABLE / HASHED | 4B37002820BEA167DAACCABEBC655C9E18BDAFF87E09ED02C8BCDBD20D3D44E1 |
| AEOS_最终资料归档_20261014_V7.2.2/02_标准与治理/本轮核查与更新候选/AEOS_V7.2_整体更新方案_M13_M14_V7.2.2.md | AVAILABLE / HASHED | 88733AEB764317596D097C822FC49C98450C7DA45EB40F6CE7BB079AFDD20B0D |

EBMS 的实施验收必须采用当前 36 周 Gate；来源资料中的专业整改项需映射为 M03 的当前 Action/Result/Evidence。 对应正式文件仍须按 System Registry V1.3 候选字段登记。

## 十一 执行输入

本方案执行输入固定为：AEOS V7.2.2 当前评审基线、9 个月/36 周计划、M01/M02/M12 安全与证据门禁、M13 Hub 与 M14 NOMI 当前边界、对应模块领域资料和经登记的 GitHub/ChatGPT 证据。
