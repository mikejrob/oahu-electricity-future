#!/usr/bin/env bash
# Push the working repo to origin AND mirror the current HEAD tree to the clean
# repository (github.com/mikejrob/oahu-electricity-future) as one fresh commit.
# The clean repo carries no development history: each sync adds a single commit
# whose tree exactly equals the working repo's HEAD tree (verified before push).
#
# NOTE: no `set -e`. On Lustre, `rm -rf` occasionally returns non-zero on a
# just-emptied directory ("Directory not empty"); that must NOT abort the sync
# (it silently stalled the mirror before). We verify success by comparing tree
# hashes, not by exit codes of the cleanup.
#
# Usage: ./push_both.sh "commit subject for the clean repo"
set -uo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
CLEAN="${CLEAN_REPO_DIR:-$(dirname "$SRC")/oahu-electricity-future}"
MSG="${1:-Sync results and report from working repository}"

cd "$SRC"
git push origin main || { echo "origin push failed"; exit 1; }
[ -d "$CLEAN/.git" ] || { echo "clean repo checkout not found at $CLEAN"; exit 1; }

# Replace the clean tree with HEAD's tree (tracked files only). Retry the wipe
# to absorb Lustre's transient non-empty errors; correctness is checked below.
for _ in 1 2 3; do
  find "$CLEAN" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} + 2>/dev/null
done
git archive HEAD | tar -x -C "$CLEAN"

cd "$CLEAN"
git add -A
# Hard correctness gate: the staged tree must equal the source HEAD tree.
CLEAN_TREE="$(git write-tree)"
SRC_TREE="$(git -C "$SRC" rev-parse HEAD^{tree})"
if [ "$CLEAN_TREE" != "$SRC_TREE" ]; then
  echo "ABORT: clean tree $CLEAN_TREE != source HEAD tree $SRC_TREE"
  exit 1
fi
if git diff --cached --quiet HEAD 2>/dev/null; then
  echo "clean repo already up to date at $(git rev-parse --short HEAD)"
else
  git commit -q -m "$MSG"
  git push origin main || { echo "clean push failed"; exit 1; }
  echo "clean repo pushed: $(git rev-parse --short HEAD)"
fi
