# ADR-2026-004: M05 消费 Keycloak 主体上下文，但不自动建号

- Status: Accepted
- Owner: owner.m00（身份平面）+ owner.m05（账号生命周期）
- Effective Date: 2026-11-18
- Supersedes: —

## Context

总纲把中央身份定为 Keycloak（OIDC），统一门户登录后携带主体访问各专业系统。M05（CRM）此前的
认证是自洽闭环：本地 `user` 表 + 自签 HS256 JWT（`backend/app/core/security.py`），
`decode_token` 只认 `settings.SECRET_KEY`，`get_current_user` 只按 `sub` 查本地 `user.id`。

这套闭环带来两个问题：

1. **身份不可跨系统复用**：用户在门户登录后仍要再登一次 CRM，M10 的免登票据
   （`backend/app/services/m10_sso.py`）也因此只能做成 HMAC 提案，打不通。
2. **租户与授权信息无处安放**：`PrincipalContextV1` 要求 `tenant_id`/`authz_version`/
   `capabilities`，自签 JWT 里没有，端点只能各自从 `user` 表推断。

引入 OIDC 时有一个必须裁决的点：**首次登录的未知主体要不要自动建号？**

## Decision

1. **验签归 M00，账号归 M05**。`app/core/oidc.py` 只做 JWKS 验签与 claims 抽取；
   `app/core/principal.py` 把 claims 映射成 `PrincipalContextV1`；账号是否存在由 M05 判断。
2. **不自动建号（no JIT provisioning）**。OIDC 令牌映射不到本地账号时返回 401
   「账号未在本系统开通」，不创建 `user` 行。理由：账号生命周期已由 M05 自己驱动
   （`person_lifecycle` 消费 M01 人员事件，负责离职改派与 `UserRole` 回收），
   若 OIDC 侧能建号，就会出现"中央身份建了、M05 权限没配"的半成品账号。
3. **通道按 alg 分流，灰度并存**。`get_current_user` 先看未验签 header 的 `alg`：
   等于 `settings.JWT_ALGORITHM`（HS256）走原自签路径；属于 `AEOS_OIDC_ALGORITHMS`
   （默认 RS256）且 `AEOS_OIDC_ENABLED` 才走 OIDC。签发方信息（iss）在验签前不可信，
   不能用来分流。
4. **映射以稳定标识为准**：`person_id` 取 `sub`，不用 `preferred_username`（会随改名变化）。
   本地账号解析顺序为用户名、邮箱，两者都要求 `deleted_at IS NULL`。
5. **角色合并 realm 级与 client 级**：Keycloak 默认把角色分两级存（`realm_access.roles`
   与 `resource_access[aud].roles`），只读一级会静默漏权；合并后仍受 M05 的
   `permission_codes` 二次收敛。
6. **主体上下文进入 `request.state`**，并以 `PrincipalContext` 依赖暴露，供需要
   `tenant_id`/`capabilities` 的端点使用；本地自签通道不产出 Principal（依赖会 401），
   避免"有 user 但没租户"的模糊状态。

## Alternatives

- **A. 自动建号（JIT）**：接入最快，但账号权限、数据范围、部门归属都没有来源，
  且与 `person_lifecycle` 的离职回收冲突（OIDC 建号后 M05 未必收到人员事件）。
- **B. 保留自签 JWT 作为唯一通道，用门户跳转传一次性票据**：就是 `m10_sso.py` 提案的做法，
  仍未解决租户与授权版本问题，且每个下游都要实现一遍票据校验。
- **C. 直接替换掉自签 JWT**：灰度期没有回退路径，Keycloak 未就绪的环境（当前 dev 全是
  `spool` 模式）会整体登不进。

## Consequences

- 正向：M05 具备消费中央身份的能力，M10 免登可以改为"门户签发 OIDC 令牌 + M05 验签"，
  不必再自造票据协议。
- 正向：`tenant_id` 有了单一来源（`AEOS_TENANT_ID`，多租户时由网关注入覆盖）。
- 负向：账号开通仍是人工/事件驱动的前置步骤，新员工首次登录会 401 而不是"自动可用"；
  这是有意的，但需要在运维手册里写明。
- 负向：`PyJWKClient` 首次验签会拉 JWKS，冷启动首个请求多一次网络往返；缓存后无影响。
- 风险：Keycloak 的 `aud` 若未配置为 CRM client，验签会失败；已在配置项
  `AEOS_OIDC_AUDIENCE` 暴露，默认留空表示不校验 aud（仅限内网 dev）。

## Rollback

`AEOS_OIDC_ENABLED=false` 即回到纯自签 JWT；`oidc.py`/`principal.py`/`deps` 的 OIDC 分支
可整体 revert，不影响既有登录与权限链路。

## Evidence

- CRM：`python -m pytest tests/test_aeos_identity.py -q` → 17 passed（含 RS256 验签、过期、
  受众/签发方错误、换密钥、未知账号拒绝、禁用账号拒绝）
- CRM：`python -m pytest -q` → 358 passed, 72 skipped
- 契约一致性：设 `AEOS_CONTRACTS_DIR` 时，`PrincipalContextV1` 的必填集合与
  `principal-context-v1.schema.json` 逐项相等，且无 schema 外键
- 提交：`6ac88ec feat(auth): accept Keycloak OIDC tokens behind the identity switch`
