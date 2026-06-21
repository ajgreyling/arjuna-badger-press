#!/usr/bin/env bash
set -euo pipefail

SERVER="${ABP_DEPLOY_SERVER:-arjunabadger.press}"
SSH_KEY="${ABP_SSH_KEY:-$HOME/.ssh/aj1}"
REMOTE_PATH="${ABP_REMOTE_PATH:-/var/www/arjunabadger.press/public/}"
REMOTE_RELOAD="${ABP_REMOTE_RELOAD:-}"
USERS_CSV="${ABP_DEPLOY_USERS:-admin,webdock,ubuntu,root}"
DRY_RUN="${ABP_DEPLOY_DRY_RUN:-1}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PUBLIC_DIR="$ROOT/site/public"

IFS=',' read -r -a USERS <<< "$USERS_CSV"

echo "=========================================="
echo "Arjuna Badger Press static deploy"
echo "=========================================="
echo "Server:      $SERVER"
echo "Remote path: $REMOTE_PATH"
echo "SSH key:     $SSH_KEY"
echo "Dry run:     $DRY_RUN"
echo ""

if [[ ! -f "$SSH_KEY" ]]; then
  echo "ERROR: SSH key not found at $SSH_KEY"
  echo "Set ABP_SSH_KEY=/path/to/key or create the key first."
  exit 1
fi

echo "Building static site..."
python3 "$ROOT/site/build.py"

if [[ ! -f "$PUBLIC_DIR/index.html" ]]; then
  echo "ERROR: build did not produce $PUBLIC_DIR/index.html"
  exit 1
fi

WORKING_USER=""
for user in "${USERS[@]}"; do
  echo "Testing SSH connection as $user..."
  if ssh -i "$SSH_KEY" -o ConnectTimeout=5 -o BatchMode=yes "$user@$SERVER" "echo ok" >/dev/null 2>&1; then
    WORKING_USER="$user"
    echo "Connected as $user"
    break
  fi
done

if [[ -z "$WORKING_USER" ]]; then
  echo ""
  echo "ERROR: Could not connect with any configured username."
  echo "Tried: $USERS_CSV"
  echo "Check DNS, server hostname, SSH key permissions, and Webdock authorized keys."
  exit 1
fi

REMOTE="$WORKING_USER@$SERVER:$REMOTE_PATH"
RSYNC_FLAGS=(-az --delete --checksum)
if [[ "$DRY_RUN" != "0" ]]; then
  RSYNC_FLAGS+=(--dry-run)
fi

echo ""
echo "Syncing site/public/ to $REMOTE"
rsync "${RSYNC_FLAGS[@]}" -e "ssh -i $SSH_KEY" "$PUBLIC_DIR/" "$REMOTE"

if [[ "$DRY_RUN" != "0" ]]; then
  echo ""
  echo "Dry run complete. No files were changed on the server."
  echo "Run with ABP_DEPLOY_DRY_RUN=0 to perform the deploy."
  exit 0
fi

if [[ -n "$REMOTE_RELOAD" ]]; then
  echo ""
  echo "Running remote reload command..."
  ssh -i "$SSH_KEY" "$WORKING_USER@$SERVER" "$REMOTE_RELOAD"
fi

echo ""
echo "Deploy complete."
