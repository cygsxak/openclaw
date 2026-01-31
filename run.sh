#!/usr/bin/env bash
set -euo pipefail

LOG_DIR=/tmp
FEISHU_DIR=/workspaces/feishu/feishu-openclaw-bridge-main
MOLT_DIR=/workspaces/clawdbot

FEISHU_LOG=${LOG_DIR}/feishu-bridge.log
MOLT_LOG=${LOG_DIR}/openclaw-gateway.log
FEISHU_PID=${LOG_DIR}/feishu-bridge.pid
MOLT_PID=${LOG_DIR}/openclaw-gateway.pid

FEISHU_DEFAULT_APP_ID=cli_a9f09d8f6c38dbc2

usage() {
  cat <<EOF
Usage: $0 {start|stop|status|logs|restart}

Commands:
  start     Start both services (no-op if already running)
  stop      Stop both services (graceful then kill)
  status    Show running status and PIDs
  logs [-f] Show last 200 lines of logs; -f to follow
  restart   Stop then start
EOF
}

is_running() {
  local pidfile="$1"
  if [ -f "$pidfile" ]; then
    local pid
    pid=$(cat "$pidfile")
    if kill -0 "$pid" 2>/dev/null; then
      return 0
    else
      return 1
    fi
  fi
  return 1
}

start() {
  if is_running "$FEISHU_PID" || is_running "$MOLT_PID"; then
    echo "One or more services already running; run 'status' to see details."
    return
  fi

  echo "Starting Feishu bridge..."
  (
    cd "$FEISHU_DIR"
    env FEISHU_APP_ID=${FEISHU_APP_ID:-$FEISHU_DEFAULT_APP_ID} node bridge.mjs >> "$FEISHU_LOG" 2>&1 &
    echo $! > "$FEISHU_PID"
  )

  sleep 1

  echo "Starting openclaw gateway..."
  (
    cd "$MOLT_DIR"
    pnpm openclaw gateway run --port 18789 >> "$MOLT_LOG" 2>&1 &
    echo $! > "$MOLT_PID"
  )

  echo "Started. Logs: $FEISHU_LOG, $MOLT_LOG"
}

stop_one() {
  local pidfile="$1"; local name="$2"
  if [ ! -f "$pidfile" ]; then
    echo "$name pidfile not found: $pidfile"
    return
  fi
  local pid
  pid=$(cat "$pidfile")
  if ! kill -0 "$pid" 2>/dev/null; then
    echo "$name (pid $pid) not running"
    rm -f "$pidfile" || true
    return
  fi
  echo "Stopping $name (pid $pid)"
  kill "$pid" 2>/dev/null || true
  for i in {1..10}; do
    if kill -0 "$pid" 2>/dev/null; then
      sleep 1
    else
      break
    fi
  done
  if kill -0 "$pid" 2>/dev/null; then
    echo "$name did not exit; killing"
    kill -9 "$pid" 2>/dev/null || true
  fi
  rm -f "$pidfile" || true
}

stop() {
  stop_one "$MOLT_PID" "openclaw gateway"
  stop_one "$FEISHU_PID" "Feishu bridge"
}

status() {
  if is_running "$FEISHU_PID"; then
    echo "Feishu bridge: running (pid $(cat $FEISHU_PID))"
  else
    echo "Feishu bridge: stopped"
  fi
  if is_running "$MOLT_PID"; then
    echo "openclaw gateway: running (pid $(cat $MOLT_PID))"
  else
    echo "openclaw gateway: stopped"
  fi
  echo "Logs: $FEISHU_LOG, $MOLT_LOG"
}

logs() {
  local follow=0
  if [ "${1-}" = "-f" ] || [ "${1-}" = "--follow" ]; then
    follow=1
  fi
  echo "--- $FEISHU_LOG ---"
  if [ $follow -eq 1 ]; then
    tail -n +1 -f "$FEISHU_LOG" &
  else
    tail -n 200 "$FEISHU_LOG" || true
  fi
  echo "--- $MOLT_LOG ---"
  if [ $follow -eq 1 ]; then
    tail -n +1 -f "$MOLT_LOG"
  else
    tail -n 200 "$MOLT_LOG" || true
  fi
}

case "${1-}" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  status)
    status
    ;;
  logs)
    logs "${2-}"
    ;;
  restart)
    stop
    start
    ;;
  ''|help|-h|--help)
    usage
    ;;
  *)
    # backward-compatible: if no args provided, behave like start
    if [ -z "${1-}" ]; then
      start
    else
      echo "Unknown command: ${1-}"
      usage
      exit 2
    fi
    ;;
esac
