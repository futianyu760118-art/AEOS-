# ADR-2026-007: 询价链路的证据平面——确认必须附可追溯证据

- Status: Accepted
- Owner: owner.m05（询价/规格书/核价/报价）、owner.m02（证据归集，后续）
- Effective Date: 2026-11-18
- Supersedes: 无

## Context

ADR-2026-006 把「销售发起 → 研发出规格书 → 财务核算 → 回销售报价」跑通了，但只回答
了「谁在什么时候把状态推到哪」，没有回答「凭什么是这个结论」。

具体缺口：

1. **确认动作可以没有依据。** `confirm_technical` / `confirm_costing` 只校验字段是否齐全、
   金额是否低于底价。研发回执填完六项参数就能点确认，财务核价填完总成本与最终价就能
   点确认——审计时问「依据哪份规格书、哪张核价单」，系统里没有答案。
2. **DEH 契约已经要求了，只是 M05 没落。** `contracts/DEH_CONTRACT_V1.md` §6 定义了
   Evidence 实体（`evidence_id` / `subject_type` / `evidence_type` / `uri` / `checksum` /
   `source_system` …），§8 明确「verification 必须关联 Result + Evidence 或有明确豁免原因」。
   `contracts/v1/finance-result-v1.schema.json` 更是要求 `evidence_refs` 至少 1 条。
3. **CRM 里已有半套设施。** `Verification`（`app/models/verification.py`，按
   `subject_type+subject_id+subject_revision` 唯一）与 `SalesResult` 的 `evidence_refs`
   已经在用，`app/services/verify.py` 也已有「passed 才算 verified」的口径。缺的是
   询价链这条业务线的接入，以及一个能存证据本身的台账。

## Decision

**1. 证据编号由 M05 服务端签发，不接受调用方自造。**

`EVD-M05-<12 位十六进制>`，格式由 `app/domain/evidence.py` 的
`EVIDENCE_ID_PATTERN` 钉死。调用方只能提交「登记的字段」，编号由服务端生成——否则
「证据」会退化成一段随便填的字符串，校验通过但毫无意义。

**2. 新建 `aeos_evidence` 台账，字段与 DEH §6 对齐。**

`evidence_id`（唯一）、`subject_type`（object/decision/action/result）、`subject_id`、
`evidence_type`（file/image/record/metric/log/approval/external_ref）、`source_system`、
`source_record_id`、`uri`、`checksum`、`version`、`confidence`、`submitted_by`、
`submitted_at`、`metadata`（列名避开 SQLAlchemy 保留字，属性名用 `meta`）、`tenant_id`、
`revision`。同一主体同一 `uri` 重复登记返回既有记录（`created=False`），不重复建。

**3. 两道硬闸门：研发回执、财务核价回执必须 ≥1 条真实存在的证据。**

- 缺证据：400「研发回执必须附证据：请上传或选择规格书/核价单等可追溯材料后再提交」；
- 编号不存在：400「研发回执引用的证据不存在：EVD-…」；
- 主体不符（拿别人的证据来凑）：400「证据 EVD-… 属于 XJ…，不能用于 研发回执」。

**4. 复用 `Verification` 做校验记录，不另造一张表。**

- 规格书确认 → `subject_type="object"`、`object_ref_type="InquirySpec"`；
- 核价确认 → `subject_type="decision"`、`object_ref_type="PricingRecord"`；
- 状态写 `passed`，`evidence_refs` 与单据同存。唯一键冲突时补写而非重复插入。

**5. 证据随事件出站。** `AEOS.Event.V2` 已有 `evidence_refs`，确认事件把本次引用的证据
一并带上，EDP 侧可据此把「询价→规格书→核价→报价」的链条串起来。

**6. 生成报价单不强制证据。** 报价单 PDF 是异步生成的，此刻要求证据会卡住主流程；
`mark_quoted` 接受可选的 `evidence_refs`，传了就校验、没传就留空。

**7. 前端只呈现、不裁决。** 面板展示证据列表、校验记录与字段来源；「能不能确认」始终由
服务端判断，前端置灰只是体验。

## Alternatives

- **A. 所有动作（含发报价、发邮件）都强制证据。** 会把销售日常动作也卡住，而报价单本身
  就是证据载体，重复要求不增加信息量。
- **B. 证据只写进 payload 的 metadata，不建台账。** 少一张表，但无法回答「这条编号到底
  存不存在、属于谁」——校验就变成字符串比对，等于没校验。
- **C. 证据直接进 M02 的 DEH，M05 只存引用。** 这是终局形态，但 M02 目前只有
  `contracts/DEH_CONTRACT_V1.md`，没有受理接口；先本地建台账并保持字段一致，后续
  整体迁移只是搬运，不用改调用方。
- **D. 允许调用方传自定义编号。** 实现最省事，但证据可伪造，闸门失效。

## Consequences

- 好处：任何一次跨系统确认都能回答「依据是什么、文件在哪、谁提交的」，审计不再靠聊天记录；
  `finance-result-v1` 的 `minItems: 1` 在 M05 侧提前满足。
- 代价：确认动作多一步「先登记证据再确认」（`POST /inquiry-flow/{id}/evidence` 再 confirm），
  前端已经把这个顺序做成按钮流程。
- 数据：`aeos_evidence` 与 `inquiry_spec.evidence_refs` / `inquiry_handoff.evidence_refs`
  三处并存——台账是证据本体，单据上的数组是「这次确认用了哪几条」，两者都必要。
- 未完成：证据还没有归集到 M02（需要 M02 开受理接口）；`checksum` 目前可选，等对象存储
  直传接通后应改为必填；证据的删除/替换策略（`deleted_at` 已留列）尚未定义业务规则。

## Rollback

`alembic downgrade aeos_inquiry_flow`（先删表与两列）。接口层保留 `evidence_refs` 的可选
入参，回滚后确认动作恢复为「只校验字段与金额」，历史事件的 `evidence_refs` 变成无主引用。

## Evidence

- CRM：`python -m pytest tests/test_inquiry_flow.py -q` → 34 passed（26 纯测 + 8 需库用例，
  含「缺证据 400」「未知编号 400」「登记幂等」「面板返回证据与校验」）。
- CRM：`python -m pytest -q`（真 PG `crm_fresh` + `AEOS_CONTRACTS_DIR`）→ 见执行进度报告。
- 迁移：`alembic heads` → 单头 `aeos_inquiry_evidence`；空库 `upgrade head` 通过。
- 规则来源：`contracts/DEH_CONTRACT_V1.md` §6/§8、`contracts/v1/finance-result-v1.schema.json`。
