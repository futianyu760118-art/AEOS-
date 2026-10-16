# AEOS Module Mapping Matrix V1.3 候选

**状态：** CANDIDATE / NOT FROZEN  
**当前执行周期：** 9 个月 / 36 周

| module_id | system_code | system_name | system_name_en | mapping_state | primary_dependencies |
| --- | --- | --- | --- | --- | --- |
| M00 | GOV | AEOS 治理与总体架构 | AEOS Governance & Architecture | Current + Target | M01/M02/M12/全体 |
| M01 | Kernel | AEOS 核心内核 | AEOS Kernel | Current + Target | M00/M01/M02/M12 |
| M02 | EDP | 企业数据与证据平台 | Enterprise Data & Evidence Platform | Current + Target | M00/M01/M02/M12 |
| M03 | EBMS | 企业经营管理系统 | Enterprise Business Management System | Current + Target | M00/M01/M02/M12 |
| M04 | RDC | 研发自治中心 | R&D Autonomous Center | Current + Target | M00/M01/M02/M12 |
| M05 | CRM | 销售自治中心 | Sales Autonomous Center | Current + Target | M00/M01/M02/M12 |
| M06 | SPC | 交付自治中心 | Delivery Autonomous Center | Current + Target | M00/M01/M02/M12 |
| M07 | HLC | 人力后勤自治中心 | Human & Logistics Center | Current + Target | M00/M01/M02/M12 |
| M08 | QAC | 质量自治中心 | Quality Autonomous Center | Current + Target | M00/M01/M02/M12 |
| M09 | FAC | 财经自治中心 | Finance Autonomous Center | Current + Target | M00/M01/M02/M12 |
| M10 | POMS | 岗位与个人运营微系统 | Role & Personal Operations Micro-system | Current + Target | M00/M01/M02/M12 |
| M11 | IHC | 集成与智能硬件接入中心 | Integration & Intelligent Hardware Center | Current + Target | M00/M01/M02/M12 |
| M12 | DSO | DevSecOps 与可观测性质量中心 | DevSecOps, Observability & Quality Center | Current + Target | M00/M01/M02/M12 |
| M13 | Hub | 智能体员工自治管理中心 | AEOS Agent Workforce Center | Current + Target | M01/M02/M12/M14/业务中心 |
| M14 | NOMI | 系统研发自治中心 | NOMI System Development Autonomous Center | Current + Target | M01/M02/M12/M13/研发中心 |

## 映射规则

- Module Mapping 只登记系统边界、当前/目标归属、依赖和 Gate，不替代各域事实 Owner。
- M05 的工程代码为 CRM，M06 的工程代码为 SPC；不得在新接口中临时创造 SAC/DAC。
- M13 只管理 Agent Workforce；M14 只管理系统研发工作；业务专业事实由 M03–M11 对应中心负责。
- 所有跨模块读写必须经过 M01 授权、M02 契约和 M12 安全质量门禁。
