#!/usr/bin/env bash
set -euo pipefail

# Build a portable offline bundle of Clever: wheels + project files
# Run this in Codespaces (with internet). Copy the output tarball to the Chromebook.

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
OUT_DIR="$ROOT_DIR/offline_bundle"
WHEEL_DIR="$OUT_DIR/wheelhouse"

# Matrix of target platforms and Python versions to support (safe defaults)
# You can override via env vars, e.g., TARGET_PLATFORMS="linux_x86_64 linux_aarch64" TARGET_PYVERS="311 312"
TARGET_PLATFORMS=${TARGET_PLATFORMS:-"linux_x86_64 linux_aarch64"}
TARGET_PYVERS=${TARGET_PYVERS:-"311 312"}

echo "📦 Preparing offline bundle in: $OUT_DIR"
rm -rf "$OUT_DIR"
mkdir -p "$WHEEL_DIR/any"

# Ensure venv and modern pip
if [ ! -d "$ROOT_DIR/.venv" ]; then
  python3 -m venv "$ROOT_DIR/.venv"
fi
source "$ROOT_DIR/.venv/bin/activate"
python -m pip install -U pip wheel

# 1) Download universal (py3-none-any) wheels without pinning a platform
echo "⬇️  Downloading universal (any) wheels…"
python -m pip download -r "$ROOT_DIR/requirements.txt" -d "$WHEEL_DIR/any" || true

# 2) Download platform-specific compiled wheels for each target
for plat in $TARGET_PLATFORMS; do
  for pyv in $TARGET_PYVERS; do
    echo "⬇️  Downloading wheels for $plat (cp$pyv)…"
    subdir="$WHEEL_DIR/$plat/cp$pyv"
    mkdir -p "$subdir"
    # Try to get prebuilt wheels only; if some packages don't have wheels for this matrix,
    # 'pip download' will skip/fail them, which is fine—we'll rely on 'any' or other cp versions.
    python -m pip download \
      --only-binary=:all: \
      --platform "$plat" \
      --implementation cp \
      --python-version "$pyv" \
      --abi "cp$pyv" \
      -r "$ROOT_DIR/requirements.txt" \
      -d "$subdir" || true
  done
done

# 3) Copy project sources (exclude heavy/irrelevant stuff)
echo "🧰 Copying project sources…"
rsync -a --delete \
  --exclude ".git" \
  --exclude ".venv" \
  --exclude "__pycache__" \
  --exclude "logs" \
  --exclude "backups" \
  --exclude "*.png" \
  --exclude "*.zip" \
  --exclude "*.bundle" \
  "$ROOT_DIR/" "$OUT_DIR/project/"

# 4) Generate an offline-safe requirements file (remove direct URLs)
echo "📝 Creating requirements-offline.txt…"
REQ_IN="$ROOT_DIR/requirements.txt"
REQ_OUT="$OUT_DIR/project/requirements-offline.txt"
EN_SM_VER=$(grep -Eo 'en_core_web_sm-([0-9]+\.[0-9]+\.[0-9]+)' "$REQ_IN" | head -n1 | sed 's/en_core_web_sm-//')
if [ -z "${EN_SM_VER:-}" ]; then EN_SM_VER="3.8.0"; fi
(
  # Replace the spaCy model direct URL with the PyPI package name (hyphenated)
  sed -E \
    -e 's#en_core_web_sm\s*@\s*https?://[^ ]+#en-core-web-sm=='"$EN_SM_VER"'#g' \
    "$REQ_IN" \
  | awk '{ if (!seen[$0]++) print }'
) > "$REQ_OUT"

# 5) Create an offline installer script that auto-detects arch + Python
echo "🔧 Writing offline_install.sh…"
INSTALL_SH="$OUT_DIR/project/offline_install.sh"
cat > "$INSTALL_SH" <<'EOS'
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
EOS
chmod +x "$INSTALL_SH"

# 6) Create tarball
echo "�🗜️  Creating tarball…"
cd "$OUT_DIR/.."
tar czf clever_offline_bundle.tgz offline_bundle
cd - >/dev/null

echo "✅ Done: $OUT_DIR/../clever_offline_bundle.tgz"
echo "Next on Chromebook (offline install):"
cat <<'EOS'
  # 1) Unpack the bundle
  tar xzf clever_offline_bundle.tgz

  # 2) Run the offline installer (auto-detects arch and Python)
  cd offline_bundle/project
  ./offline_install.sh

  # 3) (Optional) Link sync folders to Crostini shared paths
  ln -s /mnt/chromeos/MyFiles/CLEVER_AI ./Clever_Sync || true
  ln -s /mnt/chromeos/MyFiles/synaptic_hub_sync ./synaptic_hub_sync || true

  # 4) Run Clever locally (offline)
  source .venv/bin/activate
  make run

  # 5) Watch sync dirs (optional)
  make watch
EOS
