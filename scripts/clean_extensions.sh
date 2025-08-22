#!/usr/bin/env bash
set -euo pipefail
# Remove all server-side extensions in the container
rm -rf ~/.vscode-server/extensions/* ~/.vscode-server/extensionsCache/* 2>/dev/null || true
echo "Extensions removed from container."
