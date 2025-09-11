#!/usr/bin/env bash
set -euo pipefail

HERE=$(cd "$(dirname "$0")" && pwd)
WHEEL_ROOT="$HERE/../wheelhouse"

arch=$(uname -m)
case "$arch" in
  x86_64|amd64) plat="linux_x86_64" ;;
  aarch64|arm64) plat="linux_aarch64" ;;
  *) echo "❌ Unsupported arch: $arch"; exit 1 ;;
esac

pyv=$(python3 - <<'PY'
import sys
print(f"{sys.version_info.major}{sys.version_info.minor}")
PY
)

# Create venv if missing
if [ ! -d "$HERE/.venv" ]; then
  python3 -m venv "$HERE/.venv"
fi
source "$HERE/.venv/bin/activate"
python -m pip install -U pip

ANY_DIR="$WHEEL_ROOT/any"
PLAT_DIR="$WHEEL_ROOT/$plat/cp$pyv"

echo "� Using wheel sources:"
echo "  any:  $ANY_DIR"
echo "  arch: $PLAT_DIR (arch=$plat, py=cp$pyv)"

# Install using find-links so pip resolves compatible wheels automatically
python -m pip install --no-index \
  --find-links "$ANY_DIR" \
  --find-links "$PLAT_DIR" \
  -r "$HERE/requirements-offline.txt"

echo "✅ Dependencies installed offline. To run Clever:"
echo "  source $HERE/.venv/bin/activate && make -C $HERE run"
