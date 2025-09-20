#!/usr/bin/env bash
set -euo pipefail

# Why: Provide a one-shot installer for the reasoning documentation pre-commit
#       hook so contributors automatically enforce Why/Where/How tokens.
# Where: Run manually: `bash tools/install_hooks.sh` from repo root.
# How: Writes .git/hooks/pre-commit invoking verification script; idempotent rewrite.

HOOK_FILE=".git/hooks/pre-commit"
SCRIPT="tools/verify_reasoning_docs.py"

if [ ! -d .git ]; then
  echo "This does not look like the root of a git repository (.git missing)." >&2
  exit 1
fi

cat > "$HOOK_FILE" <<'EOF'
#!/usr/bin/env bash
# Clever pre-commit: enforce Why/Where/How reasoning documentation
python3 tools/verify_reasoning_docs.py || exit 1
EOF

chmod +x "$HOOK_FILE"
echo "Installed pre-commit hook -> $HOOK_FILE"
echo "On next commit, staged Python files will be checked for Why/Where/How tokens."
