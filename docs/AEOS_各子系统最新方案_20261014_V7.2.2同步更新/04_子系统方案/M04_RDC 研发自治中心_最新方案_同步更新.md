# M04 RDC 研发自治中心 最新方案

**方案版本：** V7.2.2  
**方案状态：** 当前执行候选，待对应 Owner 与 Gate 签批  
**英文名称：** R&D Autonomous Center  
**建议起始日：** 2026-10-19（PMO 签发后生效）

## 一 当前定位

研发、PLM-2、项目、BOM、测试、变更和工程 Action 的专业自治中心；M14 负责系统开发管理工作面，M04 保留研发专业事实和验收。


## 模块代码与正式名称

| 字段 | 当前冻结候选 |
| --- | --- |
| module_id | M04 |
| system_code | RDC |
| system_name | 研发自治中心 |
| system_name_en | R&D Autonomous Center |

## 全系统对象代码约束

- 数据库、Event、内部 API 统一使用 snake_case。
- 对象实体使用 PascalCase；禁止使用 `/` 合并多个实体。
- 结果验证实体统一为 `Verification`，动作统一为 `verify`。
- 每个关键对象只有一个 `fact_owner`，并区分 `record_owner`、`processor`、`consumer`、`verifier`。

## 二 当前目标

将研发需求、项目、Part/BOM、ECN、模具、3D、测试、质量和研发 Action 纳入统一事实、结果和证据链。

## 三 Own 范围

- 研发项目、需求、产品/部件、BOM、ECN、样件、测试、研发质量和研发专业 Result
- 研发事项、Action、节点、责任、验收、技术风险和研发证据
- 研发专业 Agent/Skill 的业务范围、输出质量和专业人工验收
- 研发专业数据与 M02/M14 的系统研发关联

## 四 Must Not 边界

- 不拥有 M01 身份权限、M02 Evidence、M14 系统研发流程或 M03 经营决策
- 不让 Agent 直接修改正式 BOM、ECN、发布或质量结论
- 自动化测试通过不替代工程、法规、工艺或业务责任人验收

## 五 核心对象与事实 Owner

| 对象域 | 定义 | Owner |
| --- | --- | --- |
| R&D Project/Node | 研发项目、阶段、节点、责任、依赖 | M04 |
| Part/BOM/ECN | 产品部件、物料结构、工程变更 | M04 |
| Test/QualityResult | 测试、缺陷、验证、质量结果和 Evidence | M04/M08 |
| R&D Action | 研发行动、状态、验收、回执 | M04/M02 |
| TechnicalRisk | 技术风险、影响、缓解、Owner 和期限 | M04/M00 |

## 六 接口与协作

- M14：提供系统、仓库、分支、Change、Build、Test、Release 的工程管理关联
- M12：接入 CI/CD、SAST/SCA、测试、SBOM、制品签名和环境门禁
- M02：统一研发 Object/Event/Result/Evidence/Trace
- M13：提供研发 Agent 岗位、任务、工作量、绩效和成本上下文

## 七 安全控制

- BOM、ECN、图纸、3D、工艺和测试数据按项目、岗位、租户和敏感级别隔离
- 工程变更必须关联审批、影响分析、测试和回滚/恢复措施
- Agent 只允许受控查询、草案和低风险动作；关键工程写入需人审
- 研发制品、代码、构建和部署由 M14/M12 形成供应链证据

## 八 36 周落地安排

| 周期 | Gate | 当前必须完成 |
| --- | --- | --- |
| W21–W24 | G5 | 建立研发 Agent、任务、Result、Evidence 与工程链路闭环 |
| W25–W28 | G6 | 接入 M13 Workforce 和 M14 NOMI 的工程管理工作面 |
| W29–W32 | G7 | 完成研发数据隔离、供应链、漏洞、回滚和人工接管测试 |
| W33–W36 | G8 | 完成研发复制模板、运营移交、技术债和质量 KPI |

## 九 验收标准

- 需求/项目/变更/测试/结果/证据可关联，关键工程变更可回放
- 至少一条研发闭环完成审批、构建、测试、发布或回滚
- BOM/ECN/工程文件越权、泄露和误写测试通过
- 研发专业验收和 M14 工程验收职责清晰

## 十 当前来源与证据状态

| 来源 | 状态 | SHA-256 |
| --- | --- | --- |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/研发自治中心/V1.1版/AEOS_研发自治中心_PLM-2迭代解决方案与行动计划_V1.1_2026-09-23.docx | AVAILABLE / HASHED | A9A63576904908CC1EFBD5B30BD2424457D05284E60785C714C4BAE21A701026 |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/研发自治中心/V1.1版/AEOS_研发自治中心_PLM-2开发点检与进度表_V1.1_2026-09-23.xlsx | AVAILABLE / HASHED | 50D15A4B0DFCAEFC0B0ED0749EC19FA3289E0E408BC3D3E919BEB0BD5DB6E978 |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/研发自治中心/923改善方案/AEOS_研发事项与执行中心_解决方案_V1.0_2026-09-23.docx | AVAILABLE / HASHED | 02AA0C967685BAAAEBAF211C0070C728F6DF38B41702567FA1624E2678167FF2 |

研发方案已有较强模块资料基础；本方案将其与 M13 Workforce、M14 NOMI 和 36 周 Gate 对齐，需由研发 Owner 验收。 对应正式文件仍须按 System Registry V1.3 候选字段登记。

## 十一 执行输入

本方案执行输入固定为：AEOS V7.2.2 当前评审基线、9 个月/36 周计划、M01/M02/M12 安全与证据门禁、M13 Hub 与 M14 NOMI 当前边界、对应模块领域资料和经登记的 GitHub/ChatGPT 证据。
