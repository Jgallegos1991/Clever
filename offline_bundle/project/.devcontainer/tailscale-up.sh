#!/usr/bin/env bash
set -euo pipefail

# Note: Runs in the devcontainer, not Clever's runtime. Keeps Clever offline-first.

if ! command -v tailscale >/dev/null 2>&1; then
  curl -fsSL https://tailscale.com/install.sh | sh
fi

STATE_DIR="/workspaces/projects/.devcontainer/.tailscale"
STATE_FILE="${STATE_DIR}/tailscaled.state"
mkdir -p "${STATE_DIR}"

# Restart daemon in userspace with persistent state
sudo pkill tailscaled >/dev/null 2>&1 || true
sudo nohup tailscaled \
  --tun=userspace-networking \
  --state="${STATE_FILE}" \
  >/tmp/tsd.log 2>&1 &

# Grant non-root control
sudo tailscale set --operator="${USER}" || true
sleep 1

HOST_LABEL="${TAILSCALE_HOSTNAME:-codespaces-$(hostname | cut -c1-6)}"

# First run needs an authkey; subsequent runs reuse persistent state
if [ ! -s "${STATE_FILE}" ]; then
  if [ -z "${TAILSCALE_AUTHKEY:-}" ]; then
    echo "[devcontainer] Tailscale state empty and TAILSCALE_AUTHKEY not set; skipping bring-up."
    exit 0
  fi
  tailscale up \
    --ssh \
    --accept-dns=false \
    --hostname="${HOST_LABEL}" \
    --authkey="${TAILSCALE_AUTHKEY}" \
    || true
else
  tailscale up \
    --ssh \
    --accept-dns=false \
    --hostname="${HOST_LABEL}" \
    || true
fi

tailscale status || true
