#!/usr/bin/env bash
set -euo pipefail

REMOTE_USER="root"
REMOTE_HOST="213.173.108.206"
REMOTE_PORT="10032"
SSH_KEY="${HOME}/.ssh/id_ed25519"

REMOTE_BASE="/workspace/sound-production-project"
LOCAL_BASE="/home/bmainbird/UL/sound-production/project"

mkdir -p "${LOCAL_BASE}/plots" "${LOCAL_BASE}/results"

scp -i "${SSH_KEY}" -P "${REMOTE_PORT}" -r \
  "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE}/plots/" \
  "${LOCAL_BASE}"

scp -i "${SSH_KEY}" -P "${REMOTE_PORT}" -r \
  "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE}/results/" \
  "${LOCAL_BASE}"