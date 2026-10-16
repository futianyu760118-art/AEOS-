# M12 DSO DevSecOps 与可观测性质量中心 最新方案

**方案版本：** V7.2.2  
**方案状态：** 当前执行候选，待对应 Owner 与 Gate 签批  
**英文名称：** DevSecOps, Observability & Quality Center  
**建议起始日：** 2026-10-19（PMO 签发后生效）

## 一 当前定位

AEOS 的工程基础设施、安全扫描、测试、质量、构建、制品、发布、观测、告警和恢复门禁中心。


## 模块代码与正式名称

| 字段 | 当前冻结候选 |
| --- | --- |
| module_id | M12 |
| system_code | DSO |
| system_name | DevSecOps 与可观测性质量中心 |
| system_name_en | DevSecOps, Observability & Quality Center |

## 全系统对象代码约束

- 数据库、Event、内部 API 统一使用 snake_case。
- 对象实体使用 PascalCase；禁止使用 `/` 合并多个实体。
- 结果验证实体统一为 `Verification`，动作统一为 `verify`。
- 每个关键对象只有一个 `fact_owner`，并区分 `record_owner`、`processor`、`consumer`、`verifier`。

## 二 当前目标

让 M14 和所有模块的代码、依赖、制品、部署、运行、告警和回滚具备可追溯、可阻断和可恢复能力。

## 三 Own 范围

- CI/CD、分支保护、PR、SAST、SCA、Secret Scan、容器/IaC 扫描、SBOM 和制品签名
- 测试、质量门禁、环境、配置、部署、观测、告警、日志和 Trace
- 发布审批、变更审计、回滚、备份恢复和事件响应基础设施
- 工程安全策略、门禁规则、运行可靠性、容量和成本监控

## 四 Must Not 边界

- 不拥有 M14 的研发管理业务对象和 M04 的研发专业事实
- 不以扫描通过替代业务、现场、法规或专业 Owner 验收
- 不允许生产变更、凭证或制品绕过发布门禁和审计

## 五 核心对象与事实 Owner

| 对象域 | 定义 | Owner |
| --- | --- | --- |
| Pipeline、Build | 流水线、构建、输入、环境、状态和日志 | M12 |
| Test/Scan | 测试、漏洞、质量、扫描规则、结果和例外 | M12 |
| SBOM/Artifact | 依赖、制品、签名、来源、哈希和证明 | M12 |
| Release/Deploy/Rollback | 发布、部署、环境、审批、回滚和恢复 | M12/M14 |
| Observability/Incident | 日志、指标、Trace、告警、事件和响应 | M12 |

## 六 接口与协作

- M14：接收系统研发任务，返回 Build/Test/Release/Deploy/Rollback 状态和证据
- M01：服务身份、环境权限、审批和撤权
- M02：写入工程 Evidence、Audit、Trace、Result 和风险
- M13：记录 Agent 运行资源、成本、失败、质量和熔断

## 七 安全控制

- 构建环境隔离、最小权限、短时凭证、不可变制品和签名验证
- Critical 漏洞、密钥泄露、未签名制品、来源不明和质量门禁失败阻断发布
- 运行环境非 root、只读文件系统、资源配额、网络分段和出网控制
- 备份恢复、日志保全、事件隔离、凭证撤销和人工降级可执行

## 八 36 周落地安排

| 周期 | Gate | 当前必须完成 |
| --- | --- | --- |
| W13–W16 | G3 | 接入 CI/CD、扫描、测试、观测、审计和发布门禁 |
| W17–W28 | G4–G6 | 为 M03–M11、M13、M14 提供可复用工程安全能力 |
| W29–W32 | G7 | 完成供应链、红队、灾备、恢复、人工接管和回滚演练 |
| W33–W36 | G8 | 完成运营值班、告警、容量、成本和发布移交 |

## 九 验收标准

- 所有生产制品具有 SBOM、签名、来源、构建和部署证据
- Critical=0；High 已关闭或完成授权风险接受
- 发布、回滚、备份恢复、凭证撤销和事件响应演练通过
- M14 无法绕过 M12 的扫描、质量、发布和审计门禁

## 十 当前来源与证据状态

| 来源 | 状态 | SHA-256 |
| --- | --- | --- |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/AEOS_V7.2_完整总体方案与开发治理基线.docx | AVAILABLE / HASHED | 5BA7718C8FDF915DE46B6935220C0B39AFBD720AC2351130EC5368EB6ACFC015 |
| AEOS_执行前评审方案_20261014_V7.2.2/01_执行前评审总方案/AEOS_V7.2.2_执行前评审总方案.docx | AVAILABLE / HASHED | 9463B9DB83BF01437A782F4DC4F5F56511C577645C9102F14180AC9A379A3549 |
| AEOS_团队执行资料包_20261014_V7.2.2/02_执行台账与模板/04_Gate与安全门禁检查表.md | AVAILABLE / HASHED | 2C0B771D3EF3A80F63BC4246734E9C95E5EC8C4DDF86F71FFE7FD17F9FB22D9F |

M12 的当前基线由总体开发治理与执行前安全门禁组成；实施前需要指定 M12 Owner 并锁定工具链、环境和发布证据格式。 对应正式文件仍须按 System Registry V1.3 候选字段登记。

## 十一 执行输入

本方案执行输入固定为：AEOS V7.2.2 当前评审基线、9 个月/36 周计划、M01/M02/M12 安全与证据门禁、M13 Hub 与 M14 NOMI 当前边界、对应模块领域资料和经登记的 GitHub/ChatGPT 证据。
