#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <remote-host> <ssh-port>"
  exit 1
fi

REMOTE_USER="root"
REMOTE_HOST="$1"
REMOTE_PORT="$2"
SSH_KEY="${HOME}/.ssh/id_ed25519"

REMOTE_BASE="/workspace/sound-production-project"
LOCAL_BASE="/home/bmainbird/UL/sound-production/project"

mkdir -p "${LOCAL_BASE}/plots" "${LOCAL_BASE}/results" "${LOCAL_BASE}/checkpoints"

scp -i "${SSH_KEY}" -P "${REMOTE_PORT}" -r \
  "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE}/plots/" \
  "${LOCAL_BASE}"

scp -i "${SSH_KEY}" -P "${REMOTE_PORT}" -r \
  "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE}/results/" \
  "${LOCAL_BASE}"

scp -i "${SSH_KEY}" -P "${REMOTE_PORT}" -r \
  "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE}/checkpoints/" \
  "${LOCAL_BASE}"

# Generate the site
./scripts/generate_site.py
