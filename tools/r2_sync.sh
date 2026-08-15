#!/usr/bin/env bash
# r2_sync.sh — push heavy binaries to Cloudflare R2 (bucket: arjuna-badger-prod)
# so they stop living in git. Source of truth on disk; R2 is the serving/archive copy.
#
# CREDENTIALS — never committed, never passed on the command line. Export them, or
# put them in congosky-cloud/.env (which is gitignored) and `set -a; . .env; set +a`:
#
#   BLOB_ENDPOINT=https://<accountid>.r2.cloudflarestorage.com
#   AWS_ACCESS_KEY_ID=...          # Cloudflare -> R2 -> Manage R2 API Tokens (S3-compatible)
#   AWS_SECRET_ACCESS_KEY=...
#
# The bucket is PRIVATE (see congosky-cloud/wrangler.toml). Nothing here makes an
# object public; serving stays behind the Function/Worker that already fronts it.
#
# Usage:
#   ./tools/r2_sync.sh check                 # credentials + bucket reachable, no writes
#   ./tools/r2_sync.sh plan   <profile>      # dry-run: exactly what WOULD upload
#   ./tools/r2_sync.sh push   <profile>      # upload (never deletes remote by default)
#   ./tools/r2_sync.sh verify <profile>      # compare local vs remote, report drift
#
# profiles: press-build | press-assets | platform-public
set -euo pipefail

BUCKET="arjuna-badger-prod"
REMOTE="r2"

die() { echo "error: $*" >&2; exit 1; }

# Credentials are checked only when a command actually needs the network, so
# `r2_sync.sh` with no args still prints usage on a machine with no keys.
need_creds() {
  command -v rclone >/dev/null || die "rclone not installed (brew install rclone)"
  : "${BLOB_ENDPOINT:?set BLOB_ENDPOINT (see header)}"
  : "${AWS_ACCESS_KEY_ID:?set AWS_ACCESS_KEY_ID (see header)}"
  : "${AWS_SECRET_ACCESS_KEY:?set AWS_SECRET_ACCESS_KEY (see header)}"
  # Config is supplied per-invocation via env so no secret is ever written to
  # rclone.conf or into this repo.
  export RCLONE_CONFIG_R2_TYPE=s3
  export RCLONE_CONFIG_R2_PROVIDER=Cloudflare
  export RCLONE_CONFIG_R2_ENDPOINT="$BLOB_ENDPOINT"
  export RCLONE_CONFIG_R2_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID"
  export RCLONE_CONFIG_R2_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY"
  export RCLONE_CONFIG_R2_NO_CHECK_BUCKET=true
  export RCLONE_CONFIG_R2_ACL=private
}

PRESS="$HOME/code/arjuna-badger-press"
PLATFORM="$HOME/code/arjuna-badger-platform"

# profile -> local dir, remote prefix, include filters
profile() {
  case "$1" in
    press-build)
      SRC="$PRESS/books"; PREFIX="press/build"
      FILTERS=(--include '**/build/export/**')
      ;;
    press-assets)
      SRC="$PRESS"; PREFIX="press/assets"
      FILTERS=(--include 'books/**/design/**' --include 'covers/**' --include 'brand/**')
      ;;
    platform-public)
      SRC="$PLATFORM/saas/web/public"; PREFIX="platform/public"
      FILTERS=(--include 'downloads/**' --include 'audio/**' --include 'assets/**' --include 'read/**')
      ;;
    *) die "unknown profile '$1' (press-build|press-assets|platform-public)";;
  esac
  [ -d "$SRC" ] || die "source dir missing: $SRC"
}

# Binary types only — never sweep source text into the bucket.
BIN=(--include '*.pdf' --include '*.epub' --include '*.mp3' --include '*.wav'
     --include '*.png' --include '*.jpg' --include '*.jpeg' --include '*.webp'
     --include '*.tif' --include '*.tiff' --include '*.m4b' --include '*.otf' --include '*.ttf')

cmd="${1:-}"; shift || true

case "$cmd" in
  check)
    need_creds
    echo "endpoint: $BLOB_ENDPOINT"
    echo "bucket:   $BUCKET"
    rclone lsd "$REMOTE:$BUCKET" 2>&1 | head -20 \
      && echo "OK — bucket reachable" \
      || die "cannot reach bucket (check credentials / token permissions)"
    ;;
  plan|push|verify)
    p="${1:-}"; [ -n "$p" ] || die "usage: $0 $cmd <profile>"
    need_creds
    profile "$p"
    case "$cmd" in
      plan)
        echo "DRY RUN  $SRC  ->  $REMOTE:$BUCKET/$PREFIX"
        rclone copy --dry-run --stats-one-line -v \
          "${FILTERS[@]}" "${BIN[@]}" --exclude '**' \
          "$SRC" "$REMOTE:$BUCKET/$PREFIX" 2>&1 | tail -40
        ;;
      push)
        echo "UPLOAD   $SRC  ->  $REMOTE:$BUCKET/$PREFIX"
        # --immutable + no --delete: this never removes or overwrites remote objects.
        rclone copy --progress --transfers 8 --checkers 16 --immutable \
          "${FILTERS[@]}" "${BIN[@]}" --exclude '**' \
          "$SRC" "$REMOTE:$BUCKET/$PREFIX"
        ;;
      verify)
        echo "VERIFY   $SRC  vs  $REMOTE:$BUCKET/$PREFIX"
        rclone check --one-way --combined - \
          "${FILTERS[@]}" "${BIN[@]}" --exclude '**' \
          "$SRC" "$REMOTE:$BUCKET/$PREFIX" 2>/dev/null \
          | awk '{print substr($0,1,1)}' | sort | uniq -c \
          | sed 's/^/  /;s/=/= match/;s/-/- missing on remote/;s/\*/* differs/'
        ;;
    esac
    ;;
  *)
    sed -n '2,26p' "$0"
    exit 1
    ;;
esac
