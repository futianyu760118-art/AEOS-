# ADR-2026-005: 订单事实归属以 M05 为原点，用模式开关做时间切分迁移

- Status: Accepted
- Owner: owner.m05（商务订单）/ owner.m06（交付履约）
- Effective Date: 2026-11-18
- Supersedes: —

## Context

总纲的 Owner 矩阵把**商务订单**判给 M05，M06 只负责交付履约（`订单确认 → 交付`）。
但 CRM 的实现在 2026-11-16 的 M06 集成里做成了**反向拉取**：CRM 调 SPC 的
`GET /api/v1/orders`，把订单与样品单拉进来做镜像（`backend/app/services/m06.py`）。

这不是写错代码，而是迁移期的必然：存量订单的事实一直在 SPC 里，CRM 侧只是"看得见"。
问题在于**没有任何机制记录"这一行归谁"**，于是：

- 用户在 CRM 里改了订单字段，下一次拉取被 SPC 的值覆盖回去，而用户以为改成功了；
- 没有依据判断"哪一单已经可以关掉拉取、改由 CRM 签发"；
- 一次性翻转会同时动三方（CRM 变权威、M06 变消费方、存量数据要迁移对账），
  对 12/31 的 MVP 目标风险过高。

## Decision

**1. 以 M05 为原点，但用显式模式开关迁移，而不是硬切。**

数据层：`sales_order.fact_owner`（`M05` / `M06`）记录每一行的事实归属。
迁移把这列以 `server_default='M06'` 加上去，**存量行全部回填为 M06**
（上线前 CRM 的订单只来自 SPC 拉取与 Excel 导入，前者是绝大多数）。

行为层：配置 `M05_ORDER_AUTHORITY` 取三值，语义如下。

| 模式 | 新单归属 | M06 拉取 | 对 M06 行的本地写 |
| --- | --- | --- | --- |
| `pull`（默认） | M05（CRM 自己录的单 M06 里没有） | 全量 | **放行**（与升级前完全一致） |
| `cutover` | M05 | 只拉 `M05_ORDER_CUTOVER_AT` 之前的存量单 | 拦截（409） |
| `own` | M05 | 关闭（409） | 拦截（409） |

**2. 默认必须是 `pull`。** 切换开关的价值在于"能切、能切回来"。默认改成 `cutover`
等于升级当天所有改单/删单接口开始拒绝请求——那不是迁移，那是事故。

**3. 分界时间按北京时间解释，按订单业务时间比较。** `M05_ORDER_CUTOVER_AT` 无时区
时按 +08:00 解释；比较用的是 SPC 的 `order_date`，不是 CRM 的 `created_at`
（后者是导入时间，会把十年前的订单判成新单）。业务时间缺失时**按存量处理**——
宁可多导一条旧单，也不要静默丢单。

**4. 归 M05 的行不被 M06 覆盖。** 拉取时若同号行已是 `fact_owner=M05`，直接跳过。
这条在三种模式下都生效：它保护的是"CRM 自己录的单"，与模式无关。

**5. 拉取来的行一律标 M06，`own` 模式下拒拉。** `own` 模式继续拉取会把 CRM 的
新单状态覆盖成 SPC 的旧状态，必须显式关掉，而不是"拉了但忽略"。

## Alternatives

- **A. 只写 ADR 记录"当前是过渡态例外"，不改代码**：最省事，但"哪行归谁"仍然只存在于
  人的记忆里，Owner 矩阵长期失真，且无法回答审计问题。
- **C. 一次性全量迁移，切换当天 M06 停止产出订单**：语义最干净，但对账与回滚风险最高，
  且要求 M06 在切换前就具备接收 `crm.order.confirmed` 的能力——这个能力目前不存在。

## Consequences

- 正向：每一行订单的归属可查询、可过滤、可对账；切换是一次配置变更，可灰度、可回退。
- 正向：CRM 新单从此有明确身份（M05 原点），为后续 `crm.order.confirmed → M06` 的事件
  通道准备好数据基础。
- 负向：`cutover`/`own` 模式下用户改 SPC 单会收到 409，需要在界面提示"请到 SPC 处理"；
  这属于预期的语义收敛，但要配一次用户沟通。
- 负向：`fact_owner` 与 SPC 的真实归属之间没有自动校验，靠"拉取时写入"维持；
  若有人绕过服务层直接写库，这一列会失真。
- 未完成：**M06 侧还没有接收 `crm.order.confirmed` 的端点**，因此 `own` 模式下的
  订单确认事件目前发不出去；在 M06 提供入口（或经 EDP 中转）之前，只能停在 `cutover`。

## Rollback

`M05_ORDER_AUTHORITY=pull` 即回到升级前行为；`fact_owner` 列可保留（无害）或由
`alembic downgrade aeos_order_authority` 删除。无需数据修复。

## Evidence

- CRM：`python -m pytest tests/test_order_authority.py -q` → 23 passed
  （模式解析、非法配置报错、时区边界、`accepts_pull` 三种模式、写拦截范围、
  `/orders/authority` 路由顺序）
- CRM：`python -m pytest -q`（设 `AEOS_CONTRACTS_DIR`）→ 381 passed, 72 skipped
- 迁移：`alembic heads` → 单头 `aeos_order_authority`；
  `alembic upgrade aeos_outbox_envelope:aeos_order_authority --sql` 输出
  `ADD COLUMN fact_owner VARCHAR(20) DEFAULT 'M06' NOT NULL` + 一个索引，纯增量
- 提交：`0261789 feat(orders): record order fact ownership and add the authority switch`（CRM 分支
  `aeos/p0-authority-consistency`）
