# Development Ledger V1

本文件定义仓库级统一状态机与 Gate。Excel 是导出快照；正式事实源逐步迁移到 Development Ledger + EBMS Project REPORT。

## 状态机

| 状态 | 分值 | 含义 |
|---|---:|---|
| NOT_STARTED | 0 | 无活动 |
| DESIGNING | 10 | 已有 Owner/需求/设计 |
| DEVELOPING | 35 | 代码或配置开发中 |
| IN_TEST | 60 | CI 通过并进入测试 |
| DEPLOYED | 75 | 已部署测试/生产环境 |
| VERIFYING | 90 | UAT/业务结果验证中 |
| DONE | 100 | 证据齐全 + Gate 通过 + Owner 确认 |
| BLOCKED | 冻结 | 存在阻塞，不按比例自动增长 |

## G0-G6

- G0 架构门禁：命名、边界、Data Owner、Object/API/Event/Result/Evidence 契约批准。
- G1 模块化门禁：无新增跨域 direct import/跨域写表；遗留依赖有清单和 Owner。
- G2 平台门禁：Identity/Org/Policy/Object/Event/Evidence/Audit/PostgreSQL 通过集成测试。
- G3 闭环门禁：真实业务 Fact→Event→Decision→Action→Result→Evidence 全链可追溯。
- G4 管理门禁：EBMS REPORT/TODO/Exception/Decision/Evidence 稳定。
- G5 自治门禁：Skill 评测、Data Confidence、Guard、回滚、人审责任齐备。
- G6 复制门禁：T0/Value/模板/多租户/实施方法成熟。

## DONE

关键功能必须同时满足：

Code Merged + CI Passed + Automated Test Passed + Deployed + UAT Accepted + Evidence Attached + Accountable Owner Verified。

涉及经营结果的项目还需 Business Result Verified。
