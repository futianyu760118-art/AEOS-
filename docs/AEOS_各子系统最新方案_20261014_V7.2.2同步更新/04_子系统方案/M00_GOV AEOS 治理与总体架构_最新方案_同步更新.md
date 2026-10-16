# M00 GOV AEOS 治理与总体架构 最新方案

**方案版本：** V7.2.2  
**方案状态：** 当前执行候选，待对应 Owner 与 Gate 签批  
**英文名称：** AEOS Governance & Architecture  
**建议起始日：** 2026-10-19（PMO 签发后生效）

## 一 当前定位

AEOS 的治理、标准、架构、决策和执行门禁中心。M00 不承载业务事实，负责让每个系统、模块、标准和执行动作有边界、有 Owner、有证据、有签批。


## 模块代码与正式名称

| 字段 | 当前冻结候选 |
| --- | --- |
| module_id | M00 |
| system_code | GOV |
| system_name | AEOS 治理与总体架构 |
| system_name_en | AEOS Governance & Architecture |

## 全系统对象代码约束

- 数据库、Event、内部 API 统一使用 snake_case。
- 对象实体使用 PascalCase；禁止使用 `/` 合并多个实体。
- 结果验证实体统一为 `Verification`，动作统一为 `verify`。
- 每个关键对象只有一个 `fact_owner`，并区分 `record_owner`、`processor`、`consumer`、`verifier`。

## 二 当前目标

在 9 个月/36 周执行周期内建立唯一的当前架构基线、标准状态、责任矩阵、Gate 结论和复制条件。

## 三 Own 范围

- 总体架构基线、System Registry、Module Mapping Matrix 和标准目录
- 决策、风险、变更、签批、Gate、No-Go 和放行条件
- 证据完整性规则、版本状态规则、SHA-256 manifest 规则和归档目录
- 跨系统边界冲突、职责冲突、未决项和升级规则

## 四 Must Not 边界

- 不拥有 Customer、Order、Finance、Quality、Repo 等业务或工程事实
- 不以会议结论替代正式文件、来源、版本和 SHA-256
- 不绕过 M01/M02/M12 的授权、证据和安全门禁

## 五 核心对象与事实 Owner

| 对象域 | 定义 | Owner |
| --- | --- | --- |
| ArchitectureBaseline | 当前架构版本、状态、批准人、适用范围 | M00 |
| SystemRegistry | system_id、名称、边界、Owner、Must Not、关键性 | M00/P0-01 |
| ModuleMapping | 模块 Current, Target、依赖、迁移和 Gate | M00/P0-02 |
| Decision/Risk/Change | 决策、风险、变更、期限、责任和结论 | M00 |
| Gate/Signoff/Evidence | Gate 条件、签批、证据索引、SHA-256 | M00/M02 |

## 六 接口与协作

- M01–M14：登记边界、Owner、依赖、验收和 No-Go
- PMO/Architecture Board：签发周期、Gate 和风险接受
- GitHub/ChatGPT/本地归档：只做候选线索、实现证据和文件级核验，不直接替代标准

## 七 安全控制

- 架构和标准变更采用双人复核、版本递增、签批和 manifest
- P0 安全、租户、身份、数据泄露、不可回滚问题自动进入 No-Go
- 所有 Gate 证据必须可定位到文件、来源、版本、状态和 SHA-256
- 禁止无 Owner、无验收人、无回滚路径的任务进入完成状态

## 八 36 周落地安排

| 周期 | Gate | 当前必须完成 |
| --- | --- | --- |
| W01–W04 | G0 | 确认 M00–M14 边界、Owner、Must Not、P0 和安全风险 |
| W05–W12 | G1/G2 | 冻结契约、试点、风险、签批和首条真实闭环的验收规则 |
| W13–W28 | G3–G6 | 按 Gate 管理底座、业务中心、POMS、M13、M14 的接入证据 |
| W29–W36 | G7/G8 | 安全演练、终验、运营移交、复制包和最终完整性清单 |

## 九 验收标准

- System Registry 与 Module Mapping Matrix 具有唯一当前版本、Owner、签批和 manifest
- P0-03/P0-04/P0-05、POMS V2.2、M14 来源均有责任人、截止时间和证据状态
- 每个 Gate 都有通过、保持或 No-Go 结论和可定位 Evidence
- 终验包包含 KPI、风险签收、运营移交、复制模板和 SHA-256 清单

## 十 当前来源与证据状态

| 来源 | 状态 | SHA-256 |
| --- | --- | --- |
| AEOS_执行前评审方案_20261014_V7.2.2/01_执行前评审总方案/AEOS_V7.2.2_执行前评审总方案.docx | AVAILABLE / HASHED | 9463B9DB83BF01437A782F4DC4F5F56511C577645C9102F14180AC9A379A3549 |
| AEOS_最终资料归档_20261014_V7.2.2/02_标准与治理/本轮核查与更新候选/AEOS_V7.2_整体更新方案_M13_M14_V7.2.2.md | AVAILABLE / HASHED | 88733AEB764317596D097C822FC49C98450C7DA45EB40F6CE7BB079AFDD20B0D |
| AEOS_最终资料归档_20261014_V7.2.2/02_标准与治理/本轮核查与更新候选/02_AEOS标准文件权威源与版本矩阵.md | AVAILABLE / HASHED | 9E6D38D648EC8D1FD11DB422201AB2FC519DDF8F6C014A78B48D18768CC0ACDD |

正式冻结前需完成架构负责人、PMO 和各模块 Owner 的签批；本方案提供执行控制，不替代签批本身。 对应正式文件仍须按 System Registry V1.3 候选字段登记。

## 十一 执行输入

本方案执行输入固定为：AEOS V7.2.2 当前评审基线、9 个月/36 周计划、M01/M02/M12 安全与证据门禁、M13 Hub 与 M14 NOMI 当前边界、对应模块领域资料和经登记的 GitHub/ChatGPT 证据。
