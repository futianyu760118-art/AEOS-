# System Registry V1

状态：P0 基线草案  
来源：AEOS V7.2 分模块分阶段具体执行方案 V1.0

| 编号 | 模块 | 一年内目标 |
|---|---|---|
| M00 | 项目治理与架构控制 | 保证所有系统按同一基线执行，不再产生新的耦合和重复建设 |
| M01 | AEOS Kernel | 组织、身份、目标、权限、事件、任务、决策、Guard、Agent/Skill/Memory 等共享内核 |
| M02 | Enterprise Data & Evidence Platform | MDM、Business Object、Event/Evidence、数据服务、审计、Value 数据底座 |
| M03 | EBMS 企业经营管理与决策系统 | 管理者 RESULT / EXCEPTION / DECISION / EVIDENCE 主工作面 |
| M03A | EBMS·产销自治模块 | 跨销售/研发/交付/品质/财经的经营感知、风险、方案和决策闭环 |
| M04 | 研发自治中心 | 需求→设计→验证→BOM→ECO→Release→技术转移 |
| M05 | 销售自治中心 | 线索→客户→询价→报价→商务→订单→客户经营 |
| M06 | 交付自治中心 | 订单→需求→物料→采购→计划→生产→品质→物流→交付 |
| M07 | 人才与后勤服务中心（恒聘通） | 招聘/入职/培训/考勤/行政/资产/后勤服务，组织主数据引用 AEOS |
| M08 | 品控自治中心 | 来料/过程/成品/测试/CAPA/客诉/放行 Guard |
| M09 | 财经自治中心 | 收入/成本/毛利/现金/预算/应收应付/ROI/Value |
| M10 | POMS 岗位个人操作微系统 | 1 Kernel + N Role Templates + Personal Context，面向执行者 |
| M11 | 集成与智能硬件接入 | API Gateway、Connector、Event Bus、Device Gateway、PLC/设备接口 |
| M12 | DevSecOps / Observability / QA | CI/CD、自动测试、发布门禁、日志指标追踪、安全与 SLO |

## 一级红线

- M03 EBMS 不继续膨胀成超级 ERP；专业算法由专业中心提供。
- M02 统一数据不等于超级数据库；禁止各系统直接跨域写表。
- M01 不建设重型“万能平台”；LLM 不得自判权限或直接写重大正式数据。
- M10 必须是 1 Kernel + N Role Templates，不允许“一人一套代码”。
- M11 禁止 LLM 直接控制设备；安全联锁保留在 PLC/设备层。
- M12 无测试证据不得进入 Done。
