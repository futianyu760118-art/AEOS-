# M13 Hub 智能体员工自治管理中心 最新方案

**方案版本：** V7.2.2  
**方案状态：** 当前执行候选，待对应 Owner 与 Gate 签批  
**英文名称：** AEOS Agent Workforce Center  
**建议起始日：** 2026-10-19（PMO 签发后生效）

## 一 当前定位

面向 Agent 员工/Agent Workforce 的自治管理平台，类似人员管理平台，负责 Agent 的组织、岗位、能力、生命周期、运行、工作量、SLA、绩效、成本和退出。


## 模块代码与正式名称

| 字段 | 当前冻结候选 |
| --- | --- |
| module_id | M13 |
| system_code | Hub |
| system_name | 智能体员工自治管理中心 |
| system_name_en | AEOS Agent Workforce Center |

## 全系统对象代码约束

- 数据库、Event、内部 API 统一使用 snake_case。
- 对象实体使用 PascalCase；禁止使用 `/` 合并多个实体。
- 结果验证实体统一为 `Verification`，动作统一为 `verify`。
- 每个关键对象只有一个 `fact_owner`，并区分 `record_owner`、`processor`、`consumer`、`verifier`。

## 二 当前目标

建立 Agent 从登记、岗位绑定、配置、训练/评测、启用、排班、运行、暂停、转岗、降权、人工接管到退出的完整管理闭环。

## 三 Own 范围

- Agent 员工档案、agent_id、岗位绑定、团队关系、Skill/Model/Prompt/Tool 版本引用
- Lead Agent、Specialist Agent、Agent Team、工作负载、任务分派和排班
- Runtime、Workload、SLA、失败、重试、熔断、绩效、质量、成本和版本评测
- Agent 在 M03–M10、M14 中的投影、入口、生命周期和控制记录

## 四 Must Not 边界

- 不取代 M01 的 Person/Org/Position、Permission、Policy 和 Guard
- 不取代 M02 的 Object/Event/Result/Evidence/Audit 权威
- 不成为业务对象、业务结果或系统研发成果的 Owner
- 不让 Agent 绕过授权、审批、Guard、M12 门禁或人工接管

## 五 核心对象与事实 Owner

| 对象域 | 定义 | Owner |
| --- | --- | --- |
| AgentRegistry | agent_id、角色、岗位、技能、模型、Prompt、Tool、版本、Owner、状态 | M13/M01 |
| WorkforcePosition/Team | 岗位、团队、Lead, Specialist、能力、范围和成本中心 | M13/M01 |
| AgentLifecycle | 配置、训练、启用、暂停、转岗、降权、退休、退出 | M13 |
| Runtime/Workload/SLA | 运行、队列、并发、失败、重试、预算、时效和资源 | M13/M12 |
| Performance/Cost/Exit | 质量、绩效、成本、熔断、人工接管和退出证据 | M13/M02 |

## 六 接口与协作

- M01：引用 Agent identity、岗位、授权和 Guard；不得修改权限事实
- M02：记录 Agent Result、Evidence、Audit、Trace、Cost 和退出证据
- M14：提供研发 Agent 的岗位/团队/能力上下文，接收工程任务和结果
- M03–M10：提供各业务中心的 Agent 入口、工作投影、专业验收和反馈

## 七 安全控制

- 每个 Agent 使用受控身份、最小权限、租户和成本边界；工具、网络、文件、数据库和出网白名单
- Prompt Injection、间接注入、不可信内容、记忆污染、工具滥用、数据外发和越权测试
- 生产写入、发版、删除、付款、设备动作、权限提升和外部发送必须人审/双人/业务 Owner
- 预算、超时、并发、速率、熔断、隔离、凭证撤销、人工接管和证据保全可执行

## 八 36 周落地安排

| 周期 | Gate | 当前必须完成 |
| --- | --- | --- |
| W01–W04 | G0 | 确认 M13 编号、边界、Owner、Must Not、P0-01/P0-02/P0 同步和安全风险 |
| W05–W16 | G1/G3 | 完成 AgentIdentity、Registry、岗位、生命周期、Runtime、Result/Evidence 契约 |
| W21–W28 | G5/G6 | 完成三中心接入、Workforce 最小闭环、绩效成本和 M14 协作 |
| W29–W36 | G7/G8 | 完成 Agent 红队、工具治理、灾备、熔断、验收、运营和复制 |

## 九 验收标准

- Agent 生命周期可登记、启用、暂停、撤权、转岗和退出，且每一步有证据
- 高风险工具调用 100% 有策略判定、审批/人审、审计和可熔断
- Agent 工作量、SLA、质量、成本和版本可比较、可回放、可复核
- M13 与 M01/M02/M12/M14 责任边界无重叠，业务结果由专业中心验收

## 十 当前来源与证据状态

| 来源 | 状态 | SHA-256 |
| --- | --- | --- |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/Hub智能体/AEOS_Hub_M13智能体员工管理中心定位与编号决议_V1.0.md | AVAILABLE / HASHED | 5050F1EBE4D2E0B9037BCE07B04ED33AF4411573CF7212BAAA0F15FBEC385F4A |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/Hub智能体/V1.2执行版.md | AVAILABLE / HASHED | BC82BD32E08E39930A59EECB4863302364CA7D2ABE66CA8A8FA3A6380B9A20E6 |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/销售自治中心/AEOS_M05_M10_Agent_标准与总体方案_归档资料包_2026-10-10/AEOS_Agent_分层装配与治理规范_V1.0.md | AVAILABLE / HASHED | FA578EF157EE467C7E7D7C0843FC9971ADEB8FA2D8821C577E13E0514E68178A |

M13 定位与编号已纳入当前方案，但正式 P0 同步签批、Agent 工具注册、运行证据和安全红队仍是 G0/G7 放行条件。 对应正式文件仍须按 System Registry V1.3 候选字段登记。

## 十一 执行输入

本方案执行输入固定为：AEOS V7.2.2 当前评审基线、9 个月/36 周计划、M01/M02/M12 安全与证据门禁、M13 Hub 与 M14 NOMI 当前边界、对应模块领域资料和经登记的 GitHub/ChatGPT 证据。
