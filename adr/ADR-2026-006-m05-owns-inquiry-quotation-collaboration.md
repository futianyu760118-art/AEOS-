# ADR-2026-006: 询价报价协同以 M05 为编排方，M04 出规格、M09 出核价、回执进交接单

- Status: Accepted
- Owner: owner.m05（询价/报价/客户）/ owner.m04（产品配置与规格书）/ owner.m09（成本核算）
- Effective Date: 2026-11-18
- Supersedes: —

## Context

管理层要求把 EBMS（M03）里成熟的「询价 → 研发出规格书 → 财务核价 → 回销售报价」
搬到 CRM（M05），起点必须固定在销售侧，终点也必须回到销售侧的报价单。

现状是三件事拼不起来：

1. CRM 已经抄了 EBMS 的 11 个询价状态（`INQUIRY_STATUSES_V2`：`new` /
   `cert_configured` / `config_generated` / `pending_pricing` / `pending_quote` /
   `quoted` / `negotiating` / `sample` / `project` / `lost` / `closed`），
   但**只抄了状态、没抄流程**：谁该在哪个状态动手、单据交给谁、对方回了什么，
   系统里没有任何记录。结果就是"询价卡了三天"，在 CRM 里看不出卡在谁那里。
2. 财务核价其实早就有了：`pricing_record` 是版本化的核价记录（材料/人工/包装/运费/
   模具/定制/MOQ/其他/损耗/总成本/底价/建议价/最终价），还接了通用审批。
   再建一张"成本表"就是同一笔成本存两份。
3. EBMS 的规格书是 `spec_sheets`（给客户看：型号、光学、电气、结构、包装）与
   `config_sheets`（给生产看：壳体、支架、PCB、电池、包装运输）两张表，CRM 一张都没有。

## Decision

**1. 不新增询价状态，只把 11 态里的五步钉死，过程另记交接单。**

| 动作 | 起始状态 | 目标状态 | 承接系统 |
| --- | --- | --- | --- |
| `request_technical` 交研发 | `new` | `cert_configured` | M04 |
| `confirm_technical` 研发回执 | `cert_configured` | `config_generated` | M04 |
| `request_costing` 交财务 | `config_generated` | `pending_pricing` | M09 |
| `confirm_costing` 财务回执 | `pending_pricing` | `pending_quote` | M09 |
| `generate_quotation` 出报价 | `pending_quote` | `quoted` | M05 |

流程定义只在 `backend/app/domain/inquiry_flow.py` 一处（`FLOW_STEPS`），接口、校验、
前端步骤条共用这一份真相。**再叠一套并行状态会立刻出现两份真相**，这是明确拒绝的方案。

交研发这一步同时把状态推到 `cert_configured`：证书/合规配置本来就发生在销售发图之前
（EBMS 同序），合并成一次动作，避免销售为了走流程先点一个与业务无关的状态。

**2. 规格书（`inquiry_spec`）与交接单（`inquiry_handoff`）分开建表。**

- 规格书是**状态**：客户要的东西最终被研发确认成什么配置，会被报价、下单、生产反复
  引用，必须可版本（`SP-<询价号>-v<n>`），以 `confirmed` 的一版为准。
- 交接单是**过程**：每次「我把什么发给了谁、对方什么时候回、回了什么」，带
  `event_id` / `idempotency_key` / `correlation_id` / `causation_id`。发三次改两次就有三行。

**3. 财务核价复用 `pricing_record`，不新建成本表。** M09 回执直接落
`status=APPROVED` / `total_cost` / `final_price` / `approved_at`，问题记录在交接单里。

**4. 事件走 Outbox，幂等键用请求载荷指纹。** 五类事件
`InquiryTechnicalRequested` / `InquiryTechnicalConfirmed` / `InquiryCostingRequested` /
`InquiryCostingConfirmed` / `InquiryQuoted`，统一 `AEOS.Event.V2`
（`payload_version=AEOS.Inquiry.V1`，`object_type=Inquiry`）。幂等键
`M05-HANDOFF-<stage>-<inquiry_no>-<sha256(canonical payload)[:16]>`，载荷里不放时间戳，
连点两下只有一张交接单、一封下游需求。

**5. 回执先按「系统回调 + 人工代录」同一形状实现。** M04/M09 目前没有回调地址，
但业务不能等：接口由有权限的人代填回执，载荷与对端回传完全同形。对端上线后只把
调用方从人换成 EDP 转发，接口、校验、落库一行不改。

**6. 两道硬闸门，宁可 400 也不放行。**

- M04 确认规格书必须齐 6 个必备字段（型号/功率/输入电压/光通量/色温/防护等级），
  否则"规格书已确认"是空话，后续核价与生产都建立在空字段上。
- M09 回执必须给总成本与正数最终价，且不得打穿底价（底价未设则不拦——底价是风控
  字段，不是所有客户都有）。

## Alternatives

- **A. 直接调用 M04/M09 的接口，同步等待回执**：当前两个系统都没有对外接口，且
  同步调用会把研发的排期变成销售的接口超时。Outbox + 交接单能承受"对方三天后才回"。
- **C. 在 CRM 里另建一套询价状态（如 `TECH_PENDING` / `COST_PENDING`）**：
  状态数翻倍，且与 EBMS 的 11 态对不上，同步模块立刻要写映射表。否决。
- **D. 规格书只存 `params` JSONB，不建列**：省一次迁移，但型号/功率/防护等级是
  报价与生产的检索维度，必须可索引、可校验。

## Consequences

- 正向：询价单页可以回答"现在在谁手上、等了多久、上一轮回执说了什么"，销售不必再
  去微信里翻记录。
- 正向：规格书成为可版本、可引用的一等对象，为后续 M04 出图与 M06 生产准备数据。
- 正向：事件与交接单同源，EDP 侧可按 `correlation_id` 串起"询价→规格→核价→报价"整条链。
- 负向：M04/M09 尚无回调端点，现阶段回执靠人工代录，存在"代录人填错"的风险；
  缓解手段是必填校验 + 交接单留痕（谁在什么时候代录了什么）。
- 负向：`inquiry_spec` 与 EBMS 的 `spec_sheets`/`config_sheets` 是两套字段，
  迁移期需要一次字段映射（已按交集并集建列，长尾进 `params`）。
- 未完成：M04 的 `config_sheets` 专有字段（支架、PCB 型号、芯片方案、包装运输要求）
  目前只能进 `params`；若研发侧确认这些是常用项，再升列。

## Rollback

功能级回滚：不调用 `/inquiry-flow/*` 即回到"只有 11 态、没有协同"的状态，询价单
与报价单的既有接口不受影响。数据级回滚：`alembic downgrade aeos_inquiry_flow`
删除两表；`inquiry.status` 若已被推进，按 `INQUIRY_STATUS_MIGRATION` 的逆映射人工回退。

## Evidence

- CRM：`python -m pytest tests/test_inquiry_flow.py -q` → 15 passed（流程规则、
  必备字段、核价约束、载荷与幂等键）；6 个接口用例需 `CRM_TEST_DATABASE_URL`
- CRM：`python -m pytest -q`（设 `AEOS_CONTRACTS_DIR`）→ 396 passed, 78 skipped
- 迁移：`alembic heads` → 单头 `aeos_inquiry_flow`；
  `alembic upgrade aeos_order_authority:aeos_inquiry_flow --sql` 输出两张 `CREATE TABLE`
  + 索引，纯增量，不改既有表
- 来源对照：EBMS `backend/routes/inquiry.js`（`/generate-config` 284、
  `/submit-pricing` 840、`/confirm-pricing` 867、`/spec-sheet` 3336、
  `/config-sheet` 3402）；EBMS `database/database/{inquiries,spec_sheets,config_sheets}.json`
