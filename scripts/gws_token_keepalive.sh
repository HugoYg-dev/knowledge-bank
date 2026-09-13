#!/bin/bash
# gws_token_keepalive.sh — 监控 gws OAuth Token 状态并在临近 7 天过期时主动预警
#
# 在 Google Cloud Testing 模式下，refresh_token 具有 7 天（604800s）硬生命周期，
# 任何客户端 API 调用均无法突破服务端该限制。本脚本的作用：
#   1. 直接调用 getProfile 探测实际 API 鉴权状态（避免依赖 gws auth status 格式变动）
#   2. 若有效：
#      - 若已记录 last_login_epoch 且剩余时间不足 36 小时，发出预警通知
#   3. 若失效（invalid_grant / expired / revoked）：
#      - 发送 macOS 桌面弹窗提醒，告知运行 bash scripts/gws_reauth.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GWS_BIN="${GWS_BIN:-/Users/ZHao/.nvm/versions/node/v24.6.0/bin/gws}"
NOW=$(date -u +%Y-%m-%dT%H:%M:%S+00:00)
EPOCH=$(date +%s)
AUTH_STATE_FILE="$ROOT/Clippings/emails/.pipeline/auth_state.json"

export HTTP_PROXY="${HTTP_PROXY:-http://127.0.0.1:7897}"
export HTTPS_PROXY="${HTTPS_PROXY:-http://127.0.0.1:7897}"
export ALL_PROXY="${ALL_PROXY:-socks5://127.0.0.1:7897}"

mkdir -p "$(dirname "$AUTH_STATE_FILE")"

# 直接测试轻量 API 调用
API_OUTPUT=$("$GWS_BIN" gmail users getProfile --params '{"userId": "me"}' 2>&1) && API_EXIT=0 || API_EXIT=$?

if [ $API_EXIT -eq 0 ]; then
    echo "[$NOW] token_keepalive: API call succeeded, token is active"
    
    # 检查是否接近 7 天到期（Testing 模式 7 天 = 604800 秒）
    # 当剩余不足 36 小时（即已使用超过 5.5 天 = 475200 秒）时发出预警
    if [ -f "$AUTH_STATE_FILE" ]; then
        LOGIN_EPOCH=$(python3 -c "import json; d=json.load(open('$AUTH_STATE_FILE')); print(d.get('last_login_epoch', 0))" 2>/dev/null || echo 0)
        if [ "$LOGIN_EPOCH" -gt 0 ]; then
            AGE=$((EPOCH - LOGIN_EPOCH))
            # 5.5 天 = 475200 秒
            if [ $AGE -ge 475200 ]; then
                HOURS_LEFT=$(( (604800 - AGE) / 3600 ))
                if [ $HOURS_LEFT -lt 0 ]; then HOURS_LEFT=0; fi
                echo "[$NOW] token_keepalive: WARNING — Token is near 7-day expiration (~${HOURS_LEFT}h left)" >&2
                osascript -e "display notification \"Token 预计将在约 ${HOURS_LEFT} 小时后过期，请运行 bash scripts/gws_reauth.sh 续期\" with title \"⚠️ Gmail 同步即将到期\" subtitle \"knowledge-bank\"" 2>/dev/null || true
            fi
        fi
    fi
else
    echo "[$NOW] token_keepalive: API call failed (exit $API_EXIT): $API_OUTPUT" >&2
    if echo "$API_OUTPUT" | grep -E -q "invalid_grant|expired|revoked|Authentication failed"; then
        echo "[$NOW] token_keepalive: TOKEN EXPIRED — manual reauth required" >&2
        osascript -e 'display notification "OAuth Token 已过期，邮件同步暂停！请运行 bash scripts/gws_reauth.sh" with title "❌ Gmail 同步已中断" subtitle "knowledge-bank"' 2>/dev/null || true
    else
        echo "[$NOW] token_keepalive: WARNING — Network or unknown error, will retry on next schedule" >&2
    fi
fi
