#!/usr/bin/env bash
# 为自动化测试准备一个「能走 password grant」的消费方账号。
#
# 只在本地/测试 realm 使用：生产 realm 不应开启 direct access grants，
# 真实登录走浏览器授权码 + PKCE（realm 里已配 S256）。
#
# 用法（在 Keycloak 容器内执行）：
#   PASSWORD='...' /opt/keycloak/provision-e2e-user.sh
#
# 可覆盖的环境变量：KC_SERVER / KC_REALM / KC_ADMIN / KC_ADMIN_PASSWORD /
#                  CLIENT_ID / USERNAME / PASSWORD / AUDIENCE
set -euo pipefail

KC_SERVER="${KC_SERVER:-http://127.0.0.1:8080}"
KC_REALM="${KC_REALM:-aeos-dev}"
KC_ADMIN="${KC_ADMIN:-admin}"
KC_ADMIN_PASSWORD="${KC_ADMIN_PASSWORD:-admin}"
CLIENT_ID="${CLIENT_ID:-aeos-portal}"
USERNAME="${USERNAME:-sales}"
PASSWORD="${PASSWORD:?需要设置 PASSWORD（不要写进仓库）}"
AUDIENCE="${AUDIENCE:-aeos-portal}"
REALM_ROLE="${REALM_ROLE:-aeos-user}"
KCADM="${KCADM:-/opt/keycloak/bin/kcadm.sh}"

say() { printf '[provision] %s\n' "$*"; }

say "登录 master realm"
"$KCADM" config credentials \
  --server "$KC_SERVER" --realm master --user "$KC_ADMIN" --password "$KC_ADMIN_PASSWORD" >/dev/null

CLIENT_UUID="$("$KCADM" get clients -r "$KC_REALM" -q "clientId=$CLIENT_ID" --fields id --format csv --noquotes | tail -n 1)"
if [ -z "$CLIENT_UUID" ]; then
  echo "找不到 client $CLIENT_ID" >&2
  exit 1
fi
say "client $CLIENT_ID = $CLIENT_UUID"

say "开启 direct access grants（仅测试）"
"$KCADM" update "clients/$CLIENT_UUID" -r "$KC_REALM" -s directAccessGrantsEnabled=true >/dev/null

if "$KCADM" get users -r "$KC_REALM" -q "username=$USERNAME" --fields id --format csv --noquotes | tail -n 1 | grep -q .; then
  say "用户 $USERNAME 已存在，重置口令"
  "$KCADM" set-password -r "$KC_REALM" --username "$USERNAME" --new-password "$PASSWORD" >/dev/null
else
  say "创建用户 $USERNAME"
  # 必须给齐 email/firstName/lastName：Keycloak 的 user profile 把这些列为必填，
  # 缺字段的账号在 password grant 时会以 "Account is not fully set up" 拒绝。
  "$KCADM" create users -r "$KC_REALM" \
    -s "username=$USERNAME" -s enabled=true \
    -s "email=$USERNAME@example.com" -s emailVerified=true \
    -s "firstName=AEOS" -s "lastName=E2E" >/dev/null
  "$KCADM" set-password -r "$KC_REALM" --username "$USERNAME" --new-password "$PASSWORD" >/dev/null
fi

say "授予 realm 角色 $REALM_ROLE"
"$KCADM" add-roles -r "$KC_REALM" --uusername "$USERNAME" --rolename "$REALM_ROLE" >/dev/null 2>&1 || true

if "$KCADM" get "clients/$CLIENT_UUID/protocol-mappers/models" -r "$KC_REALM" --fields name --format csv --noquotes | grep -qx 'aeos-audience'; then
  say "audience mapper 已存在"
else
  say "添加 audience mapper（aud=$AUDIENCE）"
  mapper_file="$(mktemp)"
  cat >"$mapper_file" <<JSON
{
  "name": "aeos-audience",
  "protocol": "openid-connect",
  "protocolMapper": "oidc-audience-mapper",
  "consentRequired": false,
  "config": {
    "included.custom.audience": "$AUDIENCE",
    "access.token.claim": "true",
    "id.token.claim": "false",
    "introspection.token.claim": "true"
  }
}
JSON
  "$KCADM" create "clients/$CLIENT_UUID/protocol-mappers/models" -r "$KC_REALM" -f "$mapper_file" >/dev/null
  rm -f "$mapper_file"
fi

say "完成：$USERNAME 可以用 password grant 换取 $CLIENT_ID 的令牌"
