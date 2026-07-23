#!/usr/bin/env bash
# Push the working repo to origin AND mirror the current tree to the clean
# repository (github.com/mikejrob/oahu-electricity-future) as a fresh commit.
# The clean repo intentionally carries no development history: each sync adds
# one commit whose tree is exactly the working repo's HEAD tree.
#
# Usage: ./push_both.sh "commit subject for the clean repo"
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
CLEAN="${CLEAN_REPO_DIR:-$(dirname "$SRC")/oahu-electricity-future}"
MSG="${1:-Sync results and report from working repository}"

cd "$SRC"
git push origin main

[ -d "$CLEAN/.git" ] || { echo "clean repo checkout not found at $CLEAN"; exit 1; }
# replace the clean tree with HEAD's tree (tracked files only)
find "$CLEAN" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
git archive HEAD | tar -x -C "$CLEAN"
cd "$CLEAN"
git add -A
if git diff --cached --quiet; then
  echo "clean repo already up to date"
else
  git commit -q -m "$MSG"
  git push origin main
  echo "clean repo pushed: $(git rev-parse --short HEAD)"
fi
