# M01 Kernel AEOS 核心内核 最新方案

**方案版本：** V7.2.2  
**方案状态：** 当前执行候选，待对应 Owner 与 Gate 签批  
**英文名称：** AEOS Kernel  
**建议起始日：** 2026-10-19（PMO 签发后生效）

## 一 当前定位

AEOS 的身份、组织、岗位、权限、Policy 和 Guard 内核，是人、Agent、服务和设备访问系统能力的唯一授权入口。


## 模块代码与正式名称

| 字段 | 当前冻结候选 |
| --- | --- |
| module_id | M01 |
| system_code | Kernel |
| system_name | AEOS 核心内核 |
| system_name_en | AEOS Kernel |

## 全系统对象代码约束

- 数据库、Event、内部 API 统一使用 snake_case。
- 对象实体使用 PascalCase；禁止使用 `/` 合并多个实体。
- 结果验证实体统一为 `Verification`，动作统一为 `verify`。
- 每个关键对象只有一个 `fact_owner`，并区分 `record_owner`、`processor`、`consumer`、`verifier`。

## 二 当前目标

统一 person_id、org_id、position_id、agent_id、team_id、service_id 和 device_id 的引用关系，确保最小权限、租户隔离、撤权和职责分离可验证。

## 三 Own 范围

- Person/Organization/Position 的 canonical identity 引用
- Agent、服务和设备身份的注册、绑定、状态和撤销
- RBAC+ABAC、Policy、Guard、授权决定和高风险动作审批前置
- 租户、职责分离、Break-glass、撤权和权限审计

## 四 Must Not 边界

- 不拥有业务 Customer、Order、Finance、Quality 或研发成果
- 不把客户端字段、Agent 自报身份或业务角色名当作授权事实
- 不允许模块自行维护第二套权限事实或直接修改 M01 权威数据

## 五 核心对象与事实 Owner

| 对象域 | 定义 | Owner |
| --- | --- | --- |
| CanonicalIdentity | person, org, position, agent, team, service, device 的稳定引用 | M01 |
| Permission/Policy | 主体、资源、动作、条件、租户、有效期 | M01 |
| GuardDecision | 允许, 拒绝, 需人工审批、依据、策略版本 | M01/M02 |
| Grant/Revocation | 授权、撤权、原因、时间、执行结果 | M01/M02 |
| AccessAudit | 访问主体、对象、动作、结果、Trace | M01/M02 |

## 六 接口与协作

- M02：记录授权决定、撤权、特权访问和审计证据
- M13：Agent Workforce身份和岗位引用；M14：研发 Agent 和服务身份引用
- 所有业务中心：通过 API/Policy/Guard 获取授权，不直接读写权限表

## 七 安全控制

- MFA、短时凭证、服务身份轮换、默认拒绝和最小权限
- 高风险动作采用 maker-checker、双人复核或业务 Owner 确认
- 撤权、租户切换、Break-glass 和权限提升必须实时审计
- 跨租户、对象级和字段级授权测试列为 G7 前置

## 八 36 周落地安排

| 周期 | Gate | 当前必须完成 |
| --- | --- | --- |
| W05–W08 | G1 | 统一身份、岗位、Agent、服务和设备 ID；定义 Policy/Guard 契约 |
| W09–W16 | G2/G3 | 完成租户隔离、撤权、审计和共享授权底座 |
| W17–W28 | G4–G6 | 为业务中心、M13、M14 接入岗位和动作权限 |
| W29–W36 | G7/G8 | 完成越权、跨租户、密钥、人工接管和恢复演练 |

## 九 验收标准

- 关键主体和对象均可唯一引用，撤权可在运行链路生效
- RBAC+ABAC、租户隔离、对象级权限和职责分离测试通过
- 特权操作和高风险 Agent 调用 100% 有审计
- 任何模块无法绕过 M01 获得生产、资金、设备或数据导出权限

## 十 当前来源与证据状态

| 来源 | 状态 | SHA-256 |
| --- | --- | --- |
| AEOS_最终资料归档_20261014_V7.2.2/02_标准与治理/本轮核查与更新候选/AEOS_P0-01_System_Registry_V1.2_M13_M14同步候选.md | AVAILABLE / HASHED | 01E5B3389DC0C208D4A60BD514A860DD44F3E4B032E073AB31075953E342285D |
| AEOS_最终资料归档_20261014_V7.2.2/02_标准与治理/本轮核查与更新候选/AEOS_P0-02_Module_Mapping_Matrix_V1.2_M13_M14同步候选.md | AVAILABLE / HASHED | C3C4D10C8B916A795655E8C5C79599C625A5AE6AD6A4B22C06D809423A5690F6 |
| AEOS_最终资料归档_20261014_V7.2.2/02_标准与治理/本轮核查与更新候选/AEOS_P0-03_Data_Ownership.md | MISSING / EVIDENCE-PENDING |  |

P0-03 Data Ownership、P0-04 Object ID、P0-05 Contract Pack 尚需正式文件、来源、版本和 SHA-256 后进入正式矩阵。 对应正式文件仍须按 System Registry V1.3 候选字段登记。

## 十一 执行输入

本方案执行输入固定为：AEOS V7.2.2 当前评审基线、9 个月/36 周计划、M01/M02/M12 安全与证据门禁、M13 Hub 与 M14 NOMI 当前边界、对应模块领域资料和经登记的 GitHub/ChatGPT 证据。
