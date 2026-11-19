# ADR-2026-010：M05 把「交付完成」拆成业务提交与负责人确认两步

- 状态：Accepted
- 日期：2026-11-19
- 影响系统：M05 CRM（订单）、M06 SPC（订单状态回传）
- 相关：ADR-2026-005（订单事实归属开关）

## Context

订单的「交付完成」原来是一次状态流转（`POST /orders/{id}/status`）直接改成
`closed`。三个问题：

1. **责任分不清**：库里只有一个 `status`，看不出「业务说交付完了」和「负责人签字
   确认」分别是谁、什么时候做的；
2. **默认列表不实用**：一打开是全部未结束订单，跨年混在一起，业务每天要自己筛；
3. `completed` 既是「已交付」又被当作终态排除在列表外，交付完成后的单子会从视野
   里消失，负责人没人提醒去确认。

## Decision

1. `completed` 的语义定为**交付待确认**，不再是终态；只有 `closed` / `cancelled`
   算结束。
2. 交付完成分两步：
   - `POST /orders/{id}/delivery`（`order:update`）：业务提交，`status=completed`，
     写 `delivery_submitted_by/at/note`；重复提交幂等且不覆盖第一次的说明。
   - `POST /orders/{id}/delivery/confirm`（`order:status` + 负责人）：确认关闭，
     `status=closed`，写 `closed_by/at`；未提交就确认返回 409。
3. 订单列表默认「当年 + 未确认完成」，年份按 `created_at`；`year=` 翻历史，
   `all_time=true` 关掉默认；响应带 `view` 说明当前口径。
4. 五列全部可空、无默认值，存量订单不改；回滚只删列。

## Alternatives

- **A. 只加列表默认，不动状态机**：最省事，但责任仍然分不清，否决。
- **B. 新建 `delivery` 表记录每次交付**：支持多次部分交付，但当前订单是「行 + 数量」
  模型，一次交付一次确认足够；等多批次交付成为真需求再拆表。
- **C. 引入 `order:approve` 权限码**：更精确，但要在权限表里加种子数据并全量重发，
  成本大于收益；先用「`order:status` + 负责人校验」挡住越权，等组织变大再拆。
- **D. 保留 `completed` 为终态，另加 `delivered` 状态**：会多出一个与 M06 外部状态
  映射冲突的态（`EXTERNAL_ORDER_STATUS_MAP` 只有 completed/closed），否决。

## Consequences

- 好处：交付与确认各自留痕；默认视图贴近业务日常；`completed` 不再“消失”。
- 代价：`completed` 从终态变为中间态，所有把 `completed` 当结束的查询/前端判断都要
  改（已同步改 `orders.py` 的 `active` 过滤、逾期判断、前端「交期逾期」标记）。
- M06 侧：`closed` 仍是最终回传状态，语义不变；`completed` 现在会晚一些出现
  （业务提交即出现），M06 若要区分「已交付未确认」，需读 `closed_at` 是否为空。

## Owner

M05 订单模块（销售中心）。生效：2026-11-19。

## Rollback

`alembic downgrade f066a2e208cc` 删五列；接口删除两个 POST 路由即可，
`completed` 可继续用原 `POST /orders/{id}/status` 流转。
