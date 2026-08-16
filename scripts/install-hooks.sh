#!/usr/bin/env bash
# install-hooks.sh — point git at the tracked hooks. Run once per clone.
# Git does not clone hooks, so a tracked .githooks/ plus this one-liner is how a
# shared gate actually reaches every working copy.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
git config core.hooksPath .githooks
echo "core.hooksPath -> .githooks"
echo "active hooks: $(ls .githooks | tr '\n' ' ')"
