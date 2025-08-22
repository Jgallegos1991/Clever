#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON="${PYTHON:-$(command -v python || command -v python3)}"
VENV="${VENV:-.venv}"
BIN="$VENV/bin"
PY="$BIN/python"
PIP="$BIN/pip"
APP="${APP:-app.py}"
ENV_FILE="${ENV_FILE:-.env}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-5000}"

c(){ printf "\033[36m>> %s\033[0m\n" "$*"; }
die(){ printf "\033[31m!! %s\033[0m\n" "$*\n"; exit 1; }

ensure_python(){ [[ -n "${PYTHON:-}" ]] || die "No python found in PATH"; }

load_env(){ set -a; [[ -f "$ENV_FILE" ]] && source "$ENV_FILE" || true; set +a; }

cmd_setup(){
  ensure_python
  c "Creating venv with: $PYTHON"
  "$PYTHON" -m venv "$VENV"
  c "Upgrading pip"
  "$PY" -m pip install --upgrade pip
  c "Installing requirements.txt (best-effort)"
  "$PIP" install -r requirements.txt || true
  c "DB init (best-effort)"
  "$PY" - <<'PY'
try:
    from database import db_manager
    for name in ("ensure_tables","init_db"):
        if hasattr(db_manager, name): getattr(db_manager, name)()
    print("Database OK.")
except Exception as e:
    print("DB init skipped:", e)
PY
  c "Setup complete."
}

cmd_run(){
  [[ -x "$PY" ]] || die "Venv missing. Run: make setup"
  load_env
  export HOST PORT
  c "Starting Clever at http://$HOST:$PORT"
  exec "$PY" "$APP"
}

cmd_test(){
  [[ -x "$PY" ]] || die "Venv missing. Run: make setup"
  load_env
  "$PY" - <<'PY'
from app import app
with app.test_client() as c:
    r=c.get("/health"); print("GET /health", r.status_code, getattr(r,"json",None))
    r=c.post("/chat", json={"message":"hello"}); print("POST /chat", r.status_code)
    print((r.get_data(as_text=True) or "")[:200])
PY
}

cmd_urls(){ echo "http://$HOST:$PORT"; }

cmd_doctor(){
  echo "python: $(command -v python || true)"; python --version 2>&1 || true
  echo "python3: $(command -v python3 || true)"; python3 --version 2>&1 || true
  ls -la "$BIN" 2>/dev/null || echo "(no venv yet)"
}

cmd_clean-venv(){ rm -rf "$VENV"; c "Deleted $VENV"; }

case "${1:-}" in
  setup|run|test|urls|doctor|clean-venv) "cmd_$1" ;;
  *) echo "Usage: $0 {setup|run|test|urls|doctor|clean-venv}"; exit 2 ;;
esac
