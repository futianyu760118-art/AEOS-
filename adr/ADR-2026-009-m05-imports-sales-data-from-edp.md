# ADR-2026-009：M05 从 EDP 直接导入历史销售数据，订单类数据集除外

## Context

- EDP（M02）是 AEOS 的数据与证据中台，已通过 `/api/v1/data-api` 暴露只读数据集（`_catalog`、`{code}/schema`、`{code}/query`），M05 已有 `app/services/edp.py` 客户端与 `edp_sync` 全量落盘到 `edp_dataset_row`。
- 但「落盘」只是把原始 payload 存成 JSONB，业务侧无法直接使用：客户仍在 EDP 表里，CRM 里查不到、选不到、报不了价。
- 历史数据迁移与日常补数都需要一条「数据集 → CRM 业务对象」的通道。手工导出 Excel 再走通用导入可行，但把英文列名翻成中文表头这一步全靠人，且无法追溯来源数据集与批次。
- 通用导入 `app/services/data_import.py` 已具备字段校验、唯一键去重、编号生成、`overwrite` 语义；缺的只是「EDP 数据集 → 导入行」的适配层。

## Decision

1. **新增 `app/services/edp_import.py` 作为适配层**，复用通用导入，不另写一套落库逻辑：`prepare()` 取 schema 与数据 → 用别名表映射成 CRM 字段 → 以 CRM 字段中文名作列构造 `ParsedFile` → 交给 `data_import.preview/commit`。
2. **可导入的资源固定为七类**：`customers / contacts / leads / opportunities / inquiries / quotations / products`（`SALES_RESOURCES`）。资源由数据集字段自动推断（`suggest_resource` 取「必填齐全且命中最多」者），也可显式指定。
3. **订单类数据集明确不从这条通道进**：编码或标题命中 `order/订单/delivery/交付` 时 `hint_for` 返回提示「订单类数据集由 M06 同步通道维护，请走订单同步」。理由：订单的 `fact_owner` 与 `own/cutover/pull` 开关由订单归属机制统一管理（ADR-2026-005），绕过去会让归属判断失效。
4. **映射优先级三层**：显式 `mapping` > 内置英文别名表 `EN_ALIASES` > 通用导入的中文别名猜测。显式映射给出未知字段直接报错，不静默丢弃。
5. **翻页按主键 keyset**，与 `edp.query` 契约一致；取满 `limit` 而上游仍有数据时返回 `truncated=True`，界面必须提示「只导了前 N 行」，不允许把截断当全量。
6. **提交前必须先预览**：`commit()` 内部先跑 `preview()`，只要有一行不合法就整体拒绝并报出行号与原因，不做「能进的先进」的部分成功。
7. **批次留痕写 `IntegrationLog`**（`system="EDP"`、`action="IMPORT_SALES"`、`business_id=dataset_code`），记录数据集版本、映射、行数、操作人、结果；失败也留痕（`status="FAILED"` 带 `error_message`）。
8. **权限沿用业务模块**：预览要 `integration:view`，提交要目标资源自身的 `create` 权限（超管例外），不新增权限码。

## Alternatives

- **A. 只落盘不导入**（现状）：查询要人去读 JSONB，等于没解决。
- **B. 为每类资源写专用 ETL 脚本**：与通用导入两套校验逻辑，长期必然漂移。
- **C. 让 EDP 直接写 CRM 库**：违反 Data Owner 与「专业系统自治」，且跨库写无法做权限与留痕。
- **D. 导入时跳过预览直接提交**：用户看不到哪几行会失败，历史数据质量无法兜底。

## Consequences

- ✅ 一条通道覆盖七类销售主数据，字段校验与去重复用既有实现；来源可追溯到数据集与版本。
- ✅ 订单归属不被旁路，`own` 模式切换后仍然只有一条订单写入路径。
- ⚠️ `EN_ALIASES` 是「本部署的 EDP 列名风格」的硬编码，EDP 改列名时需同步维护；未命中的列会进入 `unmapped_columns` 供人工确认，不会静默丢数据。
- ⚠️ 每次提交都是全量 `preview` + 全量 `commit`，万行级数据集建议先用 `limit` 分批，再按 `overwrite` 更新。
- ⚠️ `products` 导入落到 M05 的 `product` 表，与「Product 属 M04」的 Owner 划分仍有张力，见 ADR-2026-005 的遗留项。

## Owner

M05（CRM）数据接入负责人；涉及 EDP 数据集字段变更时由 M02 会签。

## Effective Date

2026-11-19（分支 `aeos/p0-authority-consistency`）。

## Rollback

删除四条 `/api/v1/edp/imports/*` 路由与 `app/services/edp_import.py` 即可，不涉及迁移与既有数据；已导入的业务数据保留（它们已是合法 CRM 记录）。

## Evidence

- `backend/tests/test_edp_import.py`：10 个用例（8 纯测 + 2 落库），覆盖英文列映射、显式覆盖与报错、必填缺失、资源推断、订单提示、翻页与截断、缺主键、预览提交、重复导入去重、非法行整体拒绝。
- 全量：`pytest -q` → 516 passed（含真 Keycloak 两例）。
- 顺带修掉的真缺陷：`data_import.commit` 在「导入表自带客户编码」时以 `Company(**values, code=…)` 重复传参，抛 `TypeError: got multiple values for keyword argument 'code'`。
