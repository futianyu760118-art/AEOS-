# M10 POMS 岗位与个人运营微系统 最新方案

**方案版本：** V7.2.2  
**方案状态：** 当前执行候选，待对应 Owner 与 Gate 签批  
**英文名称：** Role & Personal Operations Micro-system  
**建议起始日：** 2026-10-19（PMO 签发后生效）

## 一 当前定位

岗位模板、个人上下文、待办、异常、结果和 Personal Agent 的个人操作工作面；不拥有业务主数据。


## 模块代码与正式名称

| 字段 | 当前冻结候选 |
| --- | --- |
| module_id | M10 |
| system_code | POMS |
| system_name | 岗位与个人运营微系统 |
| system_name_en | Role & Personal Operations Micro-system |

## 全系统对象代码约束

- 数据库、Event、内部 API 统一使用 snake_case。
- 对象实体使用 PascalCase；禁止使用 `/` 合并多个实体。
- 结果验证实体统一为 `Verification`，动作统一为 `verify`。
- 每个关键对象只有一个 `fact_owner`，并区分 `record_owner`、`processor`、`consumer`、`verifier`。

## 二 当前目标

为每个人和 Agent 提供受岗位、目标、权限和业务上下文约束的操作入口，将 Todo、Exception、Past Result、Personal Agent 连接到专业中心和 M02。

## 三 Own 范围

- ui_manifest、role_template_ref、personal_context、session_context、notification_state、local_pending_input、sync_state
- 岗位模板引用、个人工作面、待办、异常、通知、交互和个人结果引用
- Personal Agent 装配入口、上下文切换和个人操作体验
- POMS 与 M05/M07/M13 的个人工作关系

## 四 Must Not 边界

- 不拥有 Customer、Order、Quote、Product、Finance、Quality 等专业对象
- 不拥有 Person/Org/Position 和 Permission/Policy/Guard 的权威事实
- 不把 ChatGPT 项目线索或 M05/M10 依赖文字当作 POMS V2.2 正式原件

## 五 核心对象与事实 Owner

| 对象域 | 定义 | Owner |
| --- | --- | --- |
| RoleTemplateRef | 岗位能力、目标、权限和流程引用 | M10 引用 M01/M07 |
| PersonalContext | 个人, Agent 当前上下文、目标、工作范围 | M10 |
| Todo/Exception | 未来待办、当前异常、期限、责任和升级 | M10/M02 |
| PastResult | 过去结果的引用和证据链接 | M02 |
| PersonalAgentSession | Personal Agent 会话、工具、权限和审计 | M10/M13/M01 |

## 六 接口与协作

- M01：读取岗位、组织、权限、Policy 和 Guard，不复制权威事实
- M05/M07/M13：提供个人/Agent 工作面和任务上下文
- M02：写入 Todo、Exception、Result、Evidence、Audit 的契约记录
- M03：展示经营异常和行动，但不重复经营看板事实

## 七 安全控制

- 个人、岗位、绩效、会话和敏感上下文分级隔离
- Personal Agent 工具白名单、会话预算、记忆隔离、敏感内容脱敏和人工接管
- 本地待同步输入需加密、过期、冲突解决和审计
- 不允许通过 UI 或 Prompt 绕过 M01 权限或直接写专业库

## 八 36 周落地安排

| 周期 | Gate | 当前必须完成 |
| --- | --- | --- |
| W25–W28 | G6 | 完成 POMS 证据核验、RoleTemplate、PersonalContext、Todo/Exception/Result 最小闭环 |
| W29–W32 | G7 | 完成个人数据、会话、工具、记忆、同步和权限测试 |
| W33–W36 | G8 | 完成 POMS 运行手册、培训、验收和复制模板 |

## 九 验收标准

- POMS V2.2 具有具体文件、来源、版本、日期/状态、主格式和 SHA-256 后再进入正式矩阵
- M10 不拥有专业业务主数据，所有业务动作仍通过专业中心和 M01/M02 契约
- 个人/Agent 操作面可关联 Todo、Exception、Result、Evidence 和权限
- 同步冲突、离线输入、撤权、会话终止和记忆隔离测试通过

## 十 当前来源与证据状态

| 来源 | 状态 | SHA-256 |
| --- | --- | --- |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/销售自治中心/AEOS_M05_M10_Agent_标准与总体方案_归档资料包_2026-10-10/M05_M10_边界规范_V1.0.md | AVAILABLE / HASHED | EF33BC0A8ABB3777395F4CB0FCA18E022C083133E3D2FB6146B6B6E35C17A6DD |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/销售自治中心/AEOS_M05_M10_Agent_标准与总体方案_归档资料包_2026-10-10/AEOS_M05_M10_Agent_总体方案_V2.0.md | AVAILABLE / HASHED | B52812BDFBEACB922E63D5EACC12AAE04883BEEC54050985CF11CDAD8D101DDB |
| AEOS_最终资料归档_20261014_V7.2.2/02_标准与治理/本轮核查与更新候选/POMS_V2.2_来源核验与待加载记录_V1.1.md | AVAILABLE / HASHED | 6AA46B680B384F38F9D73CB46CB0C7A0D7A219340FBA8935C5E8677F4B64B3A2 |

POMS V2.2 当前为 PROVISIONAL / EVIDENCE-PENDING；具体文件、来源、版本和 SHA-256 未补齐前只能作为依赖候选。 对应正式文件仍须按 System Registry V1.3 候选字段登记。

## 十一 执行输入

本方案执行输入固定为：AEOS V7.2.2 当前评审基线、9 个月/36 周计划、M01/M02/M12 安全与证据门禁、M13 Hub 与 M14 NOMI 当前边界、对应模块领域资料和经登记的 GitHub/ChatGPT 证据。
