# AEOS Keycloak 开发基线

这是 AEOS 第一阶段的内网 OIDC IdP 开发基线，不是生产部署清单。它只负责登录、密码、MFA、OIDC Session、Token 和 Logout；M01 负责校验 Token、策略授权、Guard、撤权和审计。

## 启动

```powershell
Copy-Item .env.example .env
docker compose --env-file .env up -d
```

默认开发地址：`http://127.0.0.1:8080/realms/aeos-dev`。

M01 OIDC 校验配置：

```text
M01_MODE=oidc
M01_OIDC_ISSUER=http://127.0.0.1:8080/realms/aeos-dev
M01_OIDC_AUDIENCE=aeos-portal
M01_OIDC_JWKS_URI=http://127.0.0.1:8080/realms/aeos-dev/protocol/openid-connect/certs
M01_OIDC_REQUIRED_SCOPE=portal:read
```

## 约束

- `.env`、管理员密码、数据库密码和真实用户不得提交仓库。
- `start-dev`、HTTP 端口和示例回调地址仅用于本机开发；生产必须使用正式证书、反向代理、独立数据库、`start --optimized` 和 Owner/Gate 签批。
- `tenant_id` 与 `authz_version` 是用户属性映射的过渡方案，最终值由 M01 身份映射和授权版本控制；不能由浏览器请求体指定。
- `session_id` 使用 OIDC 会话上下文；M01 必须同时校验 `iss`、`aud`、`exp`、`nbf`、`sub`、租户、会话和授权版本。

