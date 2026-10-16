# M06 SPC 交付自治中心 最新方案

**方案版本：** V7.2.2  
**方案状态：** 当前执行候选，待对应 Owner 与 Gate 签批  
**英文名称：** Delivery Autonomous Center  
**建议起始日：** 2026-10-19（PMO 签发后生效）

## 一 当前定位

供应链、生产协同、交付、项目履约、容量、发运和交付质量的专业自治中心。


## 模块代码与正式名称

| 字段 | 当前冻结候选 |
| --- | --- |
| module_id | M06 |
| system_code | SPC |
| system_name | 交付自治中心 |
| system_name_en | Delivery Autonomous Center |

## 全系统对象代码约束

- 数据库、Event、内部 API 统一使用 snake_case。
- 对象实体使用 PascalCase；禁止使用 `/` 合并多个实体。
- 结果验证实体统一为 `Verification`，动作统一为 `verify`。
- 每个关键对象只有一个 `fact_owner`，并区分 `record_owner`、`processor`、`consumer`、`verifier`。

## 二 当前目标

建立订单/项目到交付任务、计划、容量、发运、异常、验收和交付 Result/Evidence 的统一闭环。

## 三 Own 范围

- Delivery Project、Delivery Task、Capacity、Shipment、Supplier/Material 状态和交付计划
- 交付风险、延期、缺料、质量和履约异常
- 交付专业 Result、验收、客户交付证据和改进 Action
- 交付 Agent/Skill 的专业边界和人工接管规则

## 四 Must Not 边界

- 不拥有销售订单、产品 BOM、财务收入/应收、质量放行或人员权限事实
- 不允许 Agent 直接变更供应商、发运、产能或客户承诺
- 不得以系统状态替代现场交付、质量或客户验收

## 五 核心对象与事实 Owner

| 对象域 | 定义 | Owner |
| --- | --- | --- |
| DeliveryProject/Task | 交付项目、任务、里程碑、责任和期限 | M06 |
| Capacity/Shipment | 产能、物料、发运、交期和执行状态 | M06 |
| DeliveryException | 延期、缺料、质量、供应商、客户和成本异常 | M06/M03 |
| DeliveryResult | 交付完成、客户验收、质量和价值结果 | M06/M02 |
| HandoverEvidence | 签收、照片、文件、验收和现场证据 | M06/M02 |

## 六 接口与协作

- M05：消费商业订单和客户承诺引用
- M04：消费产品、BOM、工程释放和变更引用
- M08/M09/M11：接收质量、成本、设备和现场接入结果
- M03/M13/M02：提交交付异常、Agent 工作负载、Result 和 Evidence

## 七 安全控制

- 供应商、客户、合同、交期、成本和现场数据分级隔离
- 发运、交期承诺、供应商切换、产能和外部通知需要审批
- 设备/现场接入通过 M11 受控网关，禁止 Agent 直接控制未登记设备
- 交付证据必须具备来源、时间、对象、责任和防篡改校验

## 八 36 周落地安排

| 周期 | Gate | 当前必须完成 |
| --- | --- | --- |
| W21–W24 | G5 | 建立交付任务、异常、结果、验收和证据闭环 |
| W25–W28 | G6 | 接入销售承诺、研发变更、质量、财务和 M13 Agent Workforce |
| W29–W32 | G7 | 完成供应商、现场、设备、数据外发、人工接管和恢复测试 |
| W33–W36 | G8 | 完成交付 KPI、复制模板、客户验收和运营移交 |

## 九 验收标准

- 至少一条交付项目从计划到验收、异常关闭和客户证据闭环
- 交期、容量、发运、质量和成本结果可关联
- 不可逆交付承诺和外部通知具有审批和审计
- 现场/设备异常具备人工接管、回滚和证据保全路径

## 十 当前来源与证据状态

| 来源 | 状态 | SHA-256 |
| --- | --- | --- |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/供应链中台/SPC供应链与生产协同中台 vs AEOS V7.2 对标评估报告 V1.0.md | AVAILABLE / HASHED | 9693A912507A9C3B7AFE69288C91902498EAA861EF546502C5766F20B26AB7A7 |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/供应链中台/SPC → AEOS M06 交付自治中心整改实施方案 V1.0.md | AVAILABLE / HASHED | BEADC78F03FD40E4F035C10ADDA25D0F431FD5783D13252EEEDA7FFEFB9AE155 |
| AEOS_最终资料归档_20261014_V7.2.2/02_标准与治理/本轮核查与更新候选/AEOS_V7.2_整体更新方案_M13_M14_V7.2.2.md | AVAILABLE / HASHED | 88733AEB764317596D097C822FC49C98450C7DA45EB40F6CE7BB079AFDD20B0D |

M06 采用供应链对标与整改资料作为当前领域输入；正式边界、Owner 和数据契约需在 G1 完成确认。 对应正式文件仍须按 System Registry V1.3 候选字段登记。

## 十一 执行输入

本方案执行输入固定为：AEOS V7.2.2 当前评审基线、9 个月/36 周计划、M01/M02/M12 安全与证据门禁、M13 Hub 与 M14 NOMI 当前边界、对应模块领域资料和经登记的 GitHub/ChatGPT 证据。
