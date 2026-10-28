# AEOS V7.2.2 — Professional Operation Surface Principle V1

状态：P0 架构执行原则  
适用范围：M04～M14 所有专业自治系统  
上位基线：AEOS V7.2.2 / System Registry / DEH Boundary

## 1. 核心原则

AEOS 正式采用：

# Professional Operation Surface Principle

定义：

> 每一个专业业务流程，都必须在其所属自治系统拥有正式、可审计、可授权、可追溯的专业操作界面。

不得因为 POMS、EBMS、Agent 能展示信息或发起动作，就取消专业系统自己的操作面。

## 2. 四层界面职责

### Domain Autonomous System
负责：
- 专业对象；
- 专业规则；
- 专业录入；
- 专业审核；
- 专业审批；
- 专业异常处理；
- 专业 Result；
- Evidence 上下文。

### M10 POMS
负责：
- Past Report；
- Future Todo；
- Personal Action；
- 待审批提示；
- 异常提醒；
- Evidence 提交入口；
- SSO Deep Link。

POMS 不复制专业系统完整表单、状态机和规则。

### M03 EBMS
负责：
- Result；
- Exception；
- Decision；
- Evidence；
- Management Analytics。

EBMS 不成为超级 ERP 或统一专业录入平台。

### Agent
负责：
- 查询；
- 解释；
- 建议；
- 草稿；
- 自动填充；
- 受控 Action 发起。

Agent 不得绕过专业系统直接写重大最终状态。

## 3. 标准运行链

```text
POMS / EBMS / Agent
        ↓
Intent / Todo / Deep Link
        ↓
Domain Operation Surface
        ↓
M01 Permission / Guard
        ↓
Professional Action
        ↓
Result
        ↓
M02 Evidence / Audit
        ↓
EBMS / POMS
```

## 4. 强制红线

### POS-GR-01
每个专业流程必须在所属自治系统有正式操作界面。

### POS-GR-02
POMS 不得复制完整专业业务逻辑。

### POS-GR-03
EBMS 不得承担专业业务录入与审批主界面。

### POS-GR-04
POMS / EBMS 的专业操作必须通过 SSO Deep Link 或标准受控 API 返回所属自治系统。

### POS-GR-05
所有审批必须在能够查看完整业务上下文、规则、风险与 Evidence 的专业界面中完成。

### POS-GR-06
Agent 不得绕过所属自治系统直接写最终业务状态。

### POS-GR-07
View / Operation / Approval / Verify 权限必须独立。

### POS-GR-08
Action 可以从 M01/POMS 发起，但专业状态变化必须由 Domain Owner System 接受并执行。

## 5. 模块示例

| 业务 | Domain Owner | 专业操作面 |
|---|---|---|
| 研发/BOM/ECO | M04 PLM | PLM |
| 客户/报价/订单商务 | M05 CRM | CRM |
| 采购/计划/生产/物流 | M06 SPC | SPC |
| 人事/行政/资产 | M07 HRM | HRM |
| 品质异常/CAPA/放行 | M08 QMS | QMS |
| 收入/成本/报销/AR/AP/付款/预算 | M09 FAC | FAC |
| 个人待办/个人反馈 | M10 POMS | POMS |

## 6. 与 DEH 的关系

DEH 负责跨模块执行闭环：

```text
Fact → Event → DecisionCase → Decision → Action → Result → Verify → Evidence
```

但 DEH 不持有专业业务主数据，也不替代 Domain Operation Surface。

## 7. SSO Deep Link 要求

专业系统应支持：
- object_ref；
- action_ref；
- task_ref；
- return_url；
- permission_context；
- correlation_id。

POMS/EBMS 点击后直接进入正确业务对象和正确操作状态。

## 8. 验收要求

任一专业模块进入 Done 前必须证明：
- 有正式专业操作界面；
- POMS 仅聚合/跳转；
- EBMS 仅消费结果；
- M01 权限与 Guard 生效；
- Evidence 可追溯；
- Agent 无越权直写；
- Contract Test 通过。

违反任一 P0 红线：

```text
NO-GO
```
