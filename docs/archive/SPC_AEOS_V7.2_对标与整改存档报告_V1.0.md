# SPC → AEOS V7.2 对标与整改存档报告 V1.0

- **被评估系统**：`futianyu760118-art/spc1`
- **对标基线**：`futianyu760118-art/AEOS-`
- **AEOS版本**：V7.2
- **目标模块**：M06 交付自治中心（Delivery Autonomy Center）
- **归档日期**：2026-09-30
- **资料性质**：代码级对标结论 + 整改实施基线 + 验收基线

---

## 1. 归档结论

当前 `spc1` 已经从早期供应链看板发展为包含订单、MRP、物料、采购、齐套、产能、排产、生产协同、交付风险、部分质量、审批、主数据、ERP集成与AI助手的综合业务平台。

经对照 AEOS V7.2 `System Registry V1` 与 `Contract Pack V1`，正式归档结论为：

> **SPC 不再继续作为独立“综合中台”横向膨胀，正式收敛为 AEOS M06 交付自治中心的核心实现。**

核心策略：

> **保留专业深度，切掉公共平台膨胀，接入 AEOS 统一底座。**

---

## 2. M06正式业务边界

M06 应聚焦：

```text
订单
→ 需求
→ MRP
→ 物料
→ 采购
→ 齐套
→ 产能
→ 排产
→ 生产
→ 交付
```

以及围绕主链的：

- 风险感知
- 异常识别
- 交付预测
- 供应协同
- 专业 Agent / Skill

M06 不应继续成为以下公共能力的 Owner：

- Enterprise Identity
- Enterprise MDM
- Finance Ledger
- Quality CAPA
- Enterprise Approval
- Enterprise Action
- Generic AI Runtime
- ERP Connector

---

## 3. 当前能力保留与迁移

### 3.1 保留并深化到 M06

- SaleOrder / SaleOrderLine
- ETAUpdate
- MaterialDemand
- PurchaseOrder
- Kitting
- MRP
- PurchaseRequisition
- Subcontract
- Capacity / UPPH
- ProductionSchedule
- ProcessProgress
- Delivery Dashboard
- Delivery Risk Engine

### 3.2 迁移或拆边界

| 当前能力 | 目标归属 | 整改动作 |
|---|---|---|
| SysUser / SysRole | M01 | 逐步迁移企业身份与角色 Owner |
| SysPermission | M01 | SPC仅保留领域权限映射 |
| UserOrgScope | M01 | 改为组织范围引用 |
| MasterData | M02 | SPC改为消费方 |
| AuditLog | M02/M12 | 接统一审计 |
| FileAsset | M02 | 逐步统一 Evidence/File |
| Approval Center | M01/DEH | 冻结通用扩展 |
| Risk Action | DEH | 从 RiskIssue 拆出 |
| QualityIssue | M08 | M06只保留交付影响字段 |
| Product Sample | M08 | Owner迁移 |
| Supplier Claim | M08/M09 | 拆分质量与财务责任 |
| Subject Balance | M09 | 迁移 |
| ERP Sync / Writeback | M11 | 迁移 Connector / Integration |
| AI Runtime | M01 | 接入统一 Agent Runtime |
| Supply Chain Skills | M06 | 保留 |

---

## 4. 关键架构问题

### 4.1 系统边界膨胀

当前 SPC 自行承载用户、权限、主数据、审批、质量、财务、AI、ERP同步/回写等公共能力，存在形成“第二个 EBMS + 第二个 Data Foundation + 第二个审批系统”的风险。

### 4.2 RiskIssue 与 Action 耦合

当前 RiskIssue 中包含：

```text
owner
action_taken
commit_date
status
```

AEOS 目标应改为：

```text
Risk Fact
↓
Event
↓
Decision
↓
Action
↓
Result
↓
Evidence
```

SPC负责发现、评分、解释和发布风险事件；DEH负责责任人、Deadline、执行、Result、Evidence、Verify。

### 4.3 QualityIssue 越界

当前 QualityIssue 已覆盖根因分析、临时措施、永久措施、审核和审批，已经进入 M08 品控自治中心职责。

M06 应只保留：

```text
order_no
quality_status
release_status
blocked_qty
expected_release_at
quality_risk
```

### 4.4 ERP直接写库

现有 `writeback_worker.py` 通过 SQL 直接 UPDATE ERP。虽然已有 queue、retry、dead、logging、backoff，但不符合 AEOS 跨域集成目标。

目标：

```text
M06
↓
Integration Request
↓
M11 Integration Facade
↓
ERP Connector
↓
ERP
```

---

## 5. 统一契约整改

第一批核心 Business Object：

```text
delivery.order
delivery.material_demand
delivery.purchase_order
delivery.mrp_run
delivery.kitting_result
delivery.production_schedule
delivery.delivery_risk
```

统一逻辑字段至少包括：

```text
tenant_id
object_type
object_id
source_system
revision
correlation_id
```

第一批标准 Event：

```text
OrderCreated
OrderChanged
OrderDeliveryRiskDetected
MaterialDemandCreated
MaterialShortageDetected
PurchaseOrderCreated
PurchaseETAChanged
PurchaseOrderDelayed
KittingCalculated
KittingShortageDetected
MRPRunCompleted
MRPExceptionDetected
ProductionScheduleCreated
ProductionScheduleChanged
ProductionScheduleDelayed
CapacityShortageDetected
QualityBlockedDelivery
DeliveryCompleted
```

第一批标准 Result：

```text
OrderDeliveryResult
MaterialReadinessResult
MRPResult
PurchaseRiskResult
ProductionScheduleResult
DeliveryRiskResult
```

关键 Result 必须支持：

```text
source
version
evidence_refs
verified_at
```

---

## 6. 12周整改实施路线

### P0：边界冻结（W1-W2）

目标：先停止横向膨胀。

执行：
- SPC正式定位 M06
- 建立 M06 Boundary
- 建立 Current → Target Mapping
- 冻结通用审批、通用主数据、通用质量、通用财务、通用AI平台扩展
- ERP直接写库列为架构红线

验收：
- 新需求进入开发前必须声明 AEOS Owner
- 跨域能力不得继续新增数据库表
- M06 / M08 / M09 / M01 / M02 / M11 边界清晰

### P1：契约改造（W3-W5）

执行：
- 7类核心对象建立 Object Contract
- 建立 Event Envelope
- RiskIssue 与 Action 开始解耦
- 至少3类 Result 标准输出
- Result 接 Evidence
- Contract Schema Test 进入 CI

### P2：公共能力解耦（W6-W9）

执行：
- Risk Event 接 DEH
- Identity 对接 M01
- MDM Owner 归 M02
- Quality 专业字段划归 M08
- Finance 专业字段划归 M09
- ERP 写回增加 Integration Facade
- 新业务代码禁止直接 ERP UPDATE

### P3：专业深化（W10-W12）

重点深化：
- MRP
- APS / Scheduling
- Kitting
- Capacity
- Purchase Risk
- Supplier Collaboration
- Delivery Prediction
- Delivery Agent

---

## 7. ERP写回整改策略

第一阶段不删除现有 Worker，先包装：

```text
SPC
↓
IntegrationFacade
↓
LegacyWritebackAdapter
↓
现有 WritebackWorker
```

新增业务代码不得再直接调用 ERP DB。

第二阶段将以下能力迁入 M11：

- ERP Credential
- SQL Template
- Retry
- Dead Letter
- Writeback Audit

SPC只提交标准：

```text
ERPWriteRequest
```

并至少包含：

```text
request_id
object_ref
command_type
payload
requested_by
requested_at
idempotency_key
status
result
```

---

## 8. Agent / Skill 整改

M06重点沉淀：

```text
MRPSkill
KittingSkill
PurchaseRiskSkill
SchedulingSkill
CapacitySkill
DeliveryRiskSkill
```

可形成：

```text
Delivery Agent
MRP Agent
Purchase Agent
Scheduling Agent
Risk Agent
```

但 Agent 不得直接：
- 修改 ERP 正式数据
- 批准重大采购
- 批准付款
- 改变正式排产
- 绕过 Guard
- 关闭重大异常

必须经过：

```text
Recommendation
↓
Decision
↓
Guard
↓
Action
```

---

## 9. 代码治理要求

整改启动后，每个 PR 必须回答：

1. 该能力属于哪个 AEOS Module？
2. 谁是数据 Owner？
3. 是否新增跨域数据库访问？
4. 是否定义 Object？
5. 是否产生 Event？
6. 是否输出 Result？
7. 是否需要 Evidence？
8. 是否需要 Guard？

无法回答清楚的 PR 不得合并。

---

## 10. 建议代码结构

逻辑收敛目标：

```text
backend/app/domain/delivery/
├── order/
├── demand/
├── mrp/
├── material/
├── purchase/
├── kitting/
├── capacity/
├── scheduling/
├── production/
├── delivery/
└── risk/
```

公共能力改为 Adapter：

```text
backend/app/adapters/
├── identity/
├── data_foundation/
├── deh/
├── quality/
├── finance/
└── integration/
```

---

## 11. P0/P1建议受控文件

AEOS主仓建议建立：

```text
architecture/M06_DELIVERY_BOUNDARY_V1.md
architecture/SPC_AEOS_MODULE_MAPPING_V1.md
contracts/M06_DELIVERY_CONTRACT_V1.md
docs/P0/SPC_M06_P0_CHECKLIST_V1.md
```

SPC仓库建议建立：

```text
docs/aeos/AEOS_ALIGNMENT.md
docs/aeos/M06_BOUNDARY.md
docs/aeos/MIGRATION_PLAN.md
docs/aeos/CONTRACT_MAPPING.md
```

---

## 12. 最终验收条件

- [ ] SPC明确为 M06
- [ ] 不再承担企业级公共平台定位
- [ ] 核心供应链/生产业务保持可用
- [ ] 核心对象实现 Object Contract
- [ ] 核心变化产生标准 Event
- [ ] Risk 与 Action 解耦
- [ ] Result 标准化
- [ ] Evidence 可追溯
- [ ] Identity 接入 M01
- [ ] MDM Owner 归 M02
- [ ] Quality 专业能力归 M08
- [ ] Finance 专业能力归 M09
- [ ] ERP 集成逐步归 M11
- [ ] 新代码禁止直接跨域写表
- [ ] Contract Test 进入 CI
- [ ] 所有关键整改有回归测试
- [ ] 原供应链生产业务不中断

---

## 13. 最终目标

SPC最终演进为：

# AEOS M06 交付自治中心

英文：

**AEOS Delivery Autonomy Center**

核心使命：

> 围绕订单交付目标，自主完成需求计算、物料保障、采购协同、产能判断、生产计划、风险预测和交付控制，并将需要人工决策的问题交由 AEOS 决策执行闭环处理。

最终业务闭环：

```text
企业目标
↓
订单
↓
需求
↓
MRP
↓
物料
↓
采购
↓
齐套
↓
产能
↓
排产
↓
生产
↓
交付
↓
Result
↓
Evidence
```

异常闭环：

```text
异常
↓
Event
↓
Decision
↓
Action
↓
Result
↓
Evidence
```

**归档判断：SPC纳入 AEOS V7.2，作为 M06 交付自治中心核心代码基线继续发展；整改重点为边界收敛、统一契约、公共能力解耦和专业能力深化。**
