#!/bin/bash
# gws_reauth.sh — 方便用户一键重新授权 Gmail
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export GWS_BIN="${GWS_BIN:-/Users/ZHao/.nvm/versions/node/v24.6.0/bin/gws}"
export HTTP_PROXY="${HTTP_PROXY:-http://127.0.0.1:7897}"
export HTTPS_PROXY="${HTTPS_PROXY:-http://127.0.0.1:7897}"
export ALL_PROXY="${ALL_PROXY:-socks5://127.0.0.1:7897}"

echo "=================================================="
echo "==> 启动 gws Gmail 授权刷新流程..."
echo "==> 提示：在 Testing 模式下，Google 限制 Token 有效期为 7 天。"
echo "==> 请在弹出的浏览器页面中完成登录授权并确认权限。"
echo "=================================================="

"$GWS_BIN" auth login -s gmail

echo "==> 正在验证授权状态..."
if "$GWS_BIN" gmail users getProfile --params '{"userId": "me"}' >/dev/null 2>&1; then
    NOW=$(date -u +%Y-%m-%dT%H:%M:%S+00:00)
    EPOCH=$(date +%s)
    AUTH_STATE_FILE="$ROOT/Clippings/emails/.pipeline/auth_state.json"
    mkdir -p "$(dirname "$AUTH_STATE_FILE")"
    cat <<EOF > "$AUTH_STATE_FILE"
{
  "last_login_at": "$NOW",
  "last_login_epoch": $EPOCH,
  "status": "valid"
}
EOF
    echo "=================================================="
    echo "==> ✅ 授权成功！已记录最新登录时间戳。"
    echo "==> 触发一次邮件同步测试..."
    uv run "$ROOT/scripts/mail_pipeline.py" run || true
    echo "=================================================="
else
    echo "=================================================="
    echo "==> ⚠️ 授权验证未通过，请检查网络连接或代理设置。"
    echo "=================================================="
    exit 1
fi
