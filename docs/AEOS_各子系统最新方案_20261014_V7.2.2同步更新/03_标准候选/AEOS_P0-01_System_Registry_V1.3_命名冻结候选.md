# AEOS System Registry V1.3 命名冻结候选

**版本：** V1.3  
**状态：** CANDIDATE / NOT FROZEN  
**适用范围：** M00–M14、System Registry、Module Mapping Matrix、架构图、GitHub、API、Event、Evidence、数据库和文件名

## 系统代码表

| module_id | system_code | system_name | system_name_en | status |
| --- | --- | --- | --- | --- |
| M00 | GOV | AEOS 治理与总体架构 | AEOS Governance & Architecture | CANDIDATE / NOT FROZEN |
| M01 | Kernel | AEOS 核心内核 | AEOS Kernel | CANDIDATE / NOT FROZEN |
| M02 | EDP | 企业数据与证据平台 | Enterprise Data & Evidence Platform | CANDIDATE / NOT FROZEN |
| M03 | EBMS | 企业经营管理系统 | Enterprise Business Management System | CANDIDATE / NOT FROZEN |
| M04 | RDC | 研发自治中心 | R&D Autonomous Center | CANDIDATE / NOT FROZEN |
| M05 | CRM | 销售自治中心 | Sales Autonomous Center | CANDIDATE / NOT FROZEN |
| M06 | SPC | 交付自治中心 | Delivery Autonomous Center | CANDIDATE / NOT FROZEN |
| M07 | HLC | 人力后勤自治中心 | Human & Logistics Center | CANDIDATE / NOT FROZEN |
| M08 | QAC | 质量自治中心 | Quality Autonomous Center | CANDIDATE / NOT FROZEN |
| M09 | FAC | 财经自治中心 | Finance Autonomous Center | CANDIDATE / NOT FROZEN |
| M10 | POMS | 岗位与个人运营微系统 | Role & Personal Operations Micro-system | CANDIDATE / NOT FROZEN |
| M11 | IHC | 集成与智能硬件接入中心 | Integration & Intelligent Hardware Center | CANDIDATE / NOT FROZEN |
| M12 | DSO | DevSecOps 与可观测性质量中心 | DevSecOps, Observability & Quality Center | CANDIDATE / NOT FROZEN |
| M13 | Hub | 智能体员工自治管理中心 | AEOS Agent Workforce Center | CANDIDATE / NOT FROZEN |
| M14 | NOMI | 系统研发自治中心 | NOMI System Development Autonomous Center | CANDIDATE / NOT FROZEN |

## 规则

- 编号 M00–M14 固定，不再重新编号。
- `system_code` 是架构、API、Event、Evidence、仓库映射和文件名的固定简称。
- M05 保留 CRM，M06 保留 SPC，作为现有工程代码使用；正式中文/英文名称仍采用本表。
- M13 保留产品品牌 AEOS Hub，系统正式简称为 Hub，英文采用 AEOS Agent Workforce Center。
- M11 的 Meeting Helper 作为 M11 IHC 的 Meeting Module，不作为一级系统。
- M14 的正式简称为 NOMI，英文不再使用 Management。
- 任何正式冻结前必须由 M00、M01、M02、M12、M13、M14 Owner 和 PMO 签批。

