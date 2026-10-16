# M14 NOMI 系统研发自治中心 最新方案

**方案版本：** V7.2.2  
**方案状态：** 当前执行候选，待对应 Owner 与 Gate 签批  
**英文名称：** NOMI System Development Autonomous Center  
**建议起始日：** 2026-10-19（PMO 签发后生效）

## 一 当前定位

AEOS 的系统开发自治管理平台，负责系统如何被规划、研发、验证、发布、运行和持续改进。M14 管系统研发工作，不管人的组织事实和业务专业事实。


## 模块代码与正式名称

| 字段 | 当前冻结候选 |
| --- | --- |
| module_id | M14 |
| system_code | NOMI |
| system_name | 系统研发自治中心 |
| system_name_en | NOMI System Development Autonomous Center |

## 全系统对象代码约束

- 数据库、Event、内部 API 统一使用 snake_case。
- 对象实体使用 PascalCase；禁止使用 `/` 合并多个实体。
- 结果验证实体统一为 `Verification`，动作统一为 `verify`。
- 每个关键对象只有一个 `fact_owner`，并区分 `record_owner`、`processor`、`consumer`、`verifier`。

## 二 当前目标

建立 System → Product/Repo → Requirement/Design → Change/Task → Build/Test → Artifact/Release → Deploy/Rollback → Incident/Debt 的全链路工程管理闭环。

## 三 Own 范围

- System、Product、Component、Repository、Branch、Environment、Criticality 和 Engineering Owner
- Requirement、Design、Task、Change、PR、Review、Approval 和计划
- Build、Test、Defect、Vulnerability、Artifact、Release、Deploy、Rollback
- 开发 Agent 编排、工程结果、技术债、性能、可靠性、安全整改和交付状态

## 四 Must Not 边界

- 不拥有 Person/Org/Position、Permission/Policy/Guard 的权威事实
- 不拥有 Customer、Order、Finance、Quality 等业务对象和业务验收
- 不自行授予开发 Agent 生产权限，不绕过 M12 扫描、质量、发布和审计
- 自动化测试通过不替代现场、法规、工艺或业务责任人验收

## 五 核心对象与事实 Owner

| 对象域 | 定义 | Owner |
| --- | --- | --- |
| System/Product/Repo | 系统、产品、组件、仓库、分支、环境、Owner、关键性 | M14 |
| Requirement/Design/Task | 需求、设计、任务、依赖、工期和责任 | M14/M04 |
| Change/PR/Approval | 变更、代码审查、审批、影响和回滚 | M14/M01 |
| Build、Test、Vulnerability | 构建、测试、质量、漏洞、缺陷和扫描结果 | M12/M14 |
| Artifact、Release、Deploy、Rollback | 制品、发布、部署、环境、回滚和恢复 | M12/M14 |
| Incident/TechnicalDebt | 事件、技术债、整改、风险和持续改进 | M14/M00 |

## 六 接口与协作

- M13：接收研发 Agent 身份、岗位、团队、能力、工作量和成本上下文
- M12：调用构建、测试、扫描、SBOM、签名、发布、观测和恢复门禁
- M01：获得服务/Agent/环境授权；不得自行授予生产权限
- M02：记录工程 Object/Event/Result/Evidence/Audit/Trace 并支持回放
- M04/M03：接收研发专业验收和经营管理引用，不替代其事实 Owner

## 七 安全控制

- 仓库、分支、PR、构建、制品和环境最小权限；短时凭证、分支保护和双人复核
- SAST、SCA、Secret Scan、容器/IaC 扫描、SBOM、制品签名、构建来源和部署证明
- 开发 Agent 工具白名单、沙箱、资源预算、出网限制、人工审批、异常熔断和生产隔离
- 发布、部署、数据迁移、权限变更、回滚和生产运维动作必须审计且可恢复

## 八 36 周落地安排

| 周期 | Gate | 当前必须完成 |
| --- | --- | --- |
| W01–W04 | G0 | 确认 M14 编号、边界、Owner、NOMI 来源证据、M13 协作和 No-Go |
| W05–W16 | G1/G3 | 完成 System/Repo/Change/Task/Build/Test/Release/Object ID 与契约、流水线门禁 |
| W17–W28 | G4–G6 | 跑通研发真实闭环并接入 M04、M13、M02、M12 和业务验收 |
| W29–W36 | G7/G8 | 供应链、红队、灾备、回滚、技术债、运营移交和终验 |

## 九 验收标准

- 需求到任务、代码/变更、构建、测试、漏洞、制品、发布、部署和回滚 100% 可关联
- 不可追溯、未签名、未扫描、未审批或不可回滚的制品不得发布
- 开发 Agent 无法绕过 M01 权限、M02 Evidence 和 M12 安全质量门禁
- M14 原始方案/正式来源、版本和 SHA-256 完成证据登记后再进入正式标准矩阵

## 十 当前来源与证据状态

| 来源 | 状态 | SHA-256 |
| --- | --- | --- |
| AEOS_执行前评审方案_20261014_V7.2.2/01_执行前评审总方案/AEOS_V7.2.2_执行前评审总方案.docx | AVAILABLE / HASHED | 9463B9DB83BF01437A782F4DC4F5F56511C577645C9102F14180AC9A379A3549 |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/研发自治中心/V1.1版/AEOS_研发自治中心_PLM-2迭代解决方案与行动计划_V1.1_2026-09-23.docx | AVAILABLE / HASHED | A9A63576904908CC1EFBD5B30BD2424457D05284E60785C714C4BAE21A701026 |
| AEOS_最终资料归档_20261014_V7.2.2/02_标准与治理/本轮核查与更新候选/03_GitHub与ChatGPT项目对照.md | AVAILABLE / HASHED | A332431D86807730E24A9EF380754D134A4B4C58B6A0F13F1C2C79F6C03536F1 |

M14 已按当前架构决策纳入 M14；NOMI 的正式方案文件、来源、版本和 SHA-256 仍需由 M14 Owner 登记并提交 G0/G6 评审。 对应正式文件仍须按 System Registry V1.3 候选字段登记。

## 十一 执行输入

本方案执行输入固定为：AEOS V7.2.2 当前评审基线、9 个月/36 周计划、M01/M02/M12 安全与证据门禁、M13 Hub 与 M14 NOMI 当前边界、对应模块领域资料和经登记的 GitHub/ChatGPT 证据。
