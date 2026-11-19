# ADR-2026-008：M05 发版前必须过门禁

- 状态：Accepted
- 日期：2026-11-19
- 相关：ADR-2026-002（M05 发布线）、ADR-2026-003（契约冻结）、`docs/AEOS_M05_RELEASE_GATE_V1.md`（CRM 仓库）

## 背景

M05 的功能已经到了「别的系统开始依赖它」的阶段：M06 要收它的订单事件、M04/M09 要回它的规格书与核价单、M00 要它消费 Keycloak 身份。但发版前的验证一直是分散的、靠人记的：契约一致性测试要手动设 `AEOS_CONTRACTS_DIR`、迁移要记得 `alembic upgrade`、前端类型检查在另一个目录、生产默认密钥没人拦。

第一次把「发版必须成立的事」写成一个脚本并真跑（2026-11-19），`migrations` 一项立刻失败：`alembic check` 报出 9 个多余索引、25 个缺失索引、9 个多余唯一约束，全部是历史迁移写完没有再校对留下的。这些漂移在本地开发里完全无感——因为开发库是 `create_all` 或增量升级出来的——但任何一次全新建库都会得到与开发库不同的结构。

## 决策

1. **发版必须过六项门禁**，写成 CRM 仓库的 `scripts/release_gate.py`，一次跑完、非零退出即阻断：契约唯一源、迁移单头且无漂移、后端全量测试（发版模式不允许跳过）、前端 `tsc --noEmit`、生产护栏、凭据扫描。
2. **生产环境 fail-fast**：`ENV` 为 `prod`/`production` 时，开发默认密钥、过短 `SECRET_KEY`、缺失的入站令牌、开启 OIDC 却没有 issuer，任一成立就拒绝启动（`core/config.py::assert_production_safe`）。宁可起不来，也不要带着默认密钥对外服务。
3. **漂移以「模型与迁移一致」为准，不以「我这台机器能跑」为准**。门禁跑 `alembic check`，不一致就失败；修法只能是补迁移或改模型，不允许靠 `create_all` 掩盖。
4. **就绪判断放在 AEOS 侧**：`scripts/check_release_readiness.py` 比对 manifest 的 `upstream_commit` 与真实 `main`、检查工作分支是否已合并、跑契约与注册表校验、检查 `sign_off`，输出「还差哪几条」而不是一句感觉。
5. **门禁脚本自己也要被测**：`backend/tests/test_release_gate.py` 覆盖解析、扫描误报、生产护栏；永远返回 PASS 的守门人比没有守门人更糟。

## 备选方案

- **只在 CI 里跑**：本仓库没有 CI（无 `.github`），且上线前往往在本机打包；先做成本地可跑、CI 再复用同一脚本。
- **只跑测试，不做漂移检查**：测试全绿但库结构已漂移是这轮真实发生的情况，测试覆盖不到 DDL 差异。
- **把 `alembic check` 的失败降级为警告**：漂移不阻断就等于没有检查；第一次跑就照出 40 余处，说明降级只会让它继续累积。
- **生产护栏放在部署侧（compose/k8s）**：部署配置五花八门，应用自己拒绝启动是最可靠的一道。

## 后果

- 发版多了一条命令的时间成本（真库全量测试约 14 秒 + 类型检查），换来「六件事同时成立」的确定结论。
- 修完漂移后，`alembic check` 从此成为常态检查，模型改动必须配迁移。
- M05 的 `lifecycle_state` 仍为 `INTEGRATING`：门禁全绿只说明「这一版可发」，READY 还需要工作分支合并进 `main`、manifest pin 更新到该提交、owner/environment 签核——三条都还没做，脚本会如实报出来。
- 回滚：门禁是只读脚本，删掉不影响运行时；生产护栏可用 `ENV` 非 `prod` 绕过（这是有意的逃生口，但不应出现在生产）。

## 证据

- CRM `scripts/release_gate.py`：六项全绿（真库 `crm_fresh`、真 Keycloak、`tsc`），494 passed / 0 skipped。
- `backend/tests/test_release_gate.py`：12 passed。
- 迁移 `aeos_gate_index_drift` + `f066a2e208cc` 之后 `No new upgrade operations detected.`
- AEOS `scripts/check_release_readiness.py` 对当前检出输出：pin 有效且对齐 main、分支领先 10 个提交未合并、签核 PENDING、状态 INTEGRATING。
