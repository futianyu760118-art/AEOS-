# M11 IHC 集成与智能硬件接入中心 最新方案

**方案版本：** V7.2.2  
**方案状态：** 当前执行候选，待对应 Owner 与 Gate 签批  
**英文名称：** Integration & Intelligent Hardware Center  
**建议起始日：** 2026-10-19（PMO 签发后生效）

## 一 当前定位

外部系统、会议、消息、智能硬件、现场和设备接入中心；将接入事件转化为受控 Event、Decision、Action、Result 和 Evidence。


## 模块代码与正式名称

| 字段 | 当前冻结候选 |
| --- | --- |
| module_id | M11 |
| system_code | IHC |
| system_name | 集成与智能硬件接入中心 |
| system_name_en | Integration & Intelligent Hardware Center |

## 全系统对象代码约束

- 数据库、Event、内部 API 统一使用 snake_case。
- 对象实体使用 PascalCase；禁止使用 `/` 合并多个实体。
- 结果验证实体统一为 `Verification`，动作统一为 `verify`。
- 每个关键对象只有一个 `fact_owner`，并区分 `record_owner`、`processor`、`consumer`、`verifier`。

## 二 当前目标

通过连接器、设备网关、会议模块和接入审计，把外部输入和现场操作纳入 AEOS 统一契约和安全控制。

## 三 Own 范围

- 连接器、Outbox、Webhook、设备身份、会议输入和现场接入适配
- Meeting/ASR/文档/图片/设备事件到 Event、Decision、Action、Evidence 的转换
- 设备/会议/现场接入的重试、幂等、授权、状态和审计
- 接入层可观测性、限流、隔离、降级和人工接管

## 四 Must Not 边界

- 不让 Meeting 成为全局业务主对象；会议输入必须降维为 AEOS Event/Decision、Action 等通用对象
- 不允许连接器直接跨域写业务库或执行未经授权的外部副作用
- 不把会议助手或设备报告直接当作所有业务系统的正式标准

## 五 核心对象与事实 Owner

| 对象域 | 定义 | Owner |
| --- | --- | --- |
| Connector/Integration | 连接器、版本、凭证、租户、状态和策略 | M11/M01 |
| Meeting/SourceEvent | 会议、ASR、文档、图片、外部事件和来源 | M11/M02 |
| Device/AccessEvent | 设备、现场、远程访问和操作事件 | M11/M02 |
| Action/Notification | 通知、任务、外部发送、现场动作 | M11/M02/M01 |
| IntegrationEvidence | 来源、时间、响应、重试、回执和审计 | M02 |

## 六 接口与协作

- M01：设备/连接器身份、权限、凭证、Guard 和租户
- M02：统一 Event、Result、Evidence、Audit、Outbox 和 Trace
- M03/M05/M06/M07/M09：接收各域通知、会议、现场和外部系统输入
- M12：运行观测、密钥、网络分段、告警和发布门禁

## 七 安全控制

- 连接器凭证存于 Secret 管理，短时化、轮换、分租户和可撤销
- 外部内容、会议转写、附件、网页和设备数据按不可信输入处理
- 设备和现场动作采用白名单、审批、人审、双人复核、限时授权和断路器
- 出网白名单、域名/地址限制、签名回执、重放保护、限流和异常隔离

## 八 36 周落地安排

| 周期 | Gate | 当前必须完成 |
| --- | --- | --- |
| W17–W20 | G4 | 完成 Meeting/Connector/Outbox 到 Decision、Action/Result/Evidence 的最小闭环 |
| W25–W28 | G6 | 接入 M05/M06/M07/M13 的通知、会议和现场证据 |
| W29–W32 | G7 | 完成凭证、Prompt Injection、出网、设备控制和恢复演练 |
| W33–W36 | G8 | 完成连接器目录、值班、告警、培训和复制包 |

## 九 验收标准

- 外部输入可追踪到来源、身份、时间、策略、Action、回执和 Evidence
- 所有外部写入、发送、设备和现场动作有审批/审计/回滚或人工接管
- 连接器重试、幂等、断网、凭证撤销和降级测试通过
- Meeting 作为接入模块服务 AEOS 通用对象，不形成平行主数据体系

## 十 当前来源与证据状态

| 来源 | 状态 | SHA-256 |
| --- | --- | --- |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/会议系统-AEOS/meeting-helper_AEOS_V7.2_适配评估正式报告_V1.0.docx | AVAILABLE / HASHED | 5BCDFB8984002099BD567EA9230162E49C7900D9721593B11436E3879636C5D2 |
| AEOS_最终资料归档_20261014_V7.2.2/03_原始资料镜像/AEOS V7.2 完整合并版deep-research-report (4).md | AVAILABLE / HASHED | 9D744BF04720564B84C540FF7BEE48DE4FB3C41044D99E4CB930E0CC3D02C438 |
| AEOS_最终资料归档_20261014_V7.2.2/02_标准与治理/本轮核查与更新候选/AEOS_V7.2_整体更新方案_M13_M14_V7.2.2.md | AVAILABLE / HASHED | 88733AEB764317596D097C822FC49C98450C7DA45EB40F6CE7BB079AFDD20B0D |

meeting-helper 适合作为 M11 的 Meeting Module/接入能力；正式接入需完成连接器、设备、凭证和安全验收。 对应正式文件仍须按 System Registry V1.3 候选字段登记。

## 十一 执行输入

本方案执行输入固定为：AEOS V7.2.2 当前评审基线、9 个月/36 周计划、M01/M02/M12 安全与证据门禁、M13 Hub 与 M14 NOMI 当前边界、对应模块领域资料和经登记的 GitHub/ChatGPT 证据。
