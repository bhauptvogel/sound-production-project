#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <ssh-port>"
  exit 1
fi

REMOTE_USER="root"
REMOTE_HOST="213.173.98.107"
REMOTE_PORT="$1"
SSH_KEY="${HOME}/.ssh/id_ed25519"

# Remote destination (where we want to copy TO)
REMOTE_BASE="/workspace/sound-production-project"
# Local source (where we are copying FROM)
LOCAL_BASE="/home/bmainbird/UL/sound-production/project"

echo "Copying clips from ${LOCAL_BASE}/clips/ to ${REMOTE_HOST}:${REMOTE_BASE}/clips/ ..."

# Using rsync for efficient delta transfer
rsync -avz -e "ssh -i ${SSH_KEY} -p ${REMOTE_PORT}" \
  --progress \
  "${LOCAL_BASE}/clips/" \
  "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE}/clips/"

echo "Clips copied successfully!"

