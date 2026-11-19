# Architecture Decision Records

每项影响一级边界、Data Owner、核心 Contract、共享底座或跨域依赖的架构决定必须建立 ADR。

建议命名：

`ADR-YYYY-NNN-short-title.md`

每份 ADR 至少包含：Context、Decision、Alternatives、Consequences、Owner、Effective Date、Rollback、Evidence。

## 索引

| ADR | 标题 | 状态 |
| --- | --- | --- |
| [ADR-2026-001](ADR-2026-001-contract-manifest-relock.md) | 契约包指纹由脚本重建，manifest 视为锁文件 | Accepted |
| [ADR-2026-002](ADR-2026-002-m05-release-line-main.md) | M05 发布线为 main | Accepted |
| [ADR-2026-003](ADR-2026-003-business-event-v1-freeze.md) | business-event-v1 保持冻结，V2 由出站边界投影 | Accepted |
| [ADR-2026-004](ADR-2026-004-m05-consumes-keycloak-principal.md) | M05 消费 Keycloak 主体上下文，但不自动建号 | Accepted |
| [ADR-2026-005](ADR-2026-005-order-fact-ownership-switch.md) | 订单事实归属以 M05 为原点，用模式开关做时间切分迁移 | Accepted |
| [ADR-2026-006](ADR-2026-006-m05-owns-inquiry-quotation-collaboration.md) | 询价报价协同以 M05 为编排方，M04 出规格、M09 出核价、回执进交接单 | Accepted |
| [ADR-2026-007](ADR-2026-007-m05-evidence-plane.md) | 询价链路的证据平面：编号服务端签发，确认必须附可追溯证据 | Accepted |
| [ADR-2026-008](ADR-2026-008-m05-release-gate.md) | M05 发版前必须过六项门禁，漂移以模型与迁移一致为准 | Accepted |
| [ADR-2026-009](ADR-2026-009-m05-imports-sales-data-from-edp.md) | 历史销售数据从 EDP 数据集导入 CRM，订单类数据集不走此通道 | Accepted |
| [ADR-2026-010](ADR-2026-010-m05-order-delivery-two-step.md) | 交付完成拆成业务提交与负责人确认两步，completed 不再是终态 | Accepted |

