#!/usr/bin/env bash
# Push the working repo to origin AND mirror the HEAD tree (minus private/)
# to the clean repository as one new commit — entirely at the git object
# level. No working-tree wipe, no archive/tar, no `git add -A`: the stripped
# tree is synthesized in a temporary index, a commit object is created with
# `git commit-tree`, and that commit is pushed straight to the mirror
# remote. This removes the Lustre metadata bottleneck that made the
# copy-based sync take minutes (and occasionally stall on rm -rf).
#
# Guards preserved from the copy-based version:
#  - ABORT if the mirror on GitHub carries commits this script did not
#    produce (user web edits are directives; port them first, then advance
#    refs/mirror-synced as instructed by the abort message).
#  - The pushed tree is by construction HEAD-minus-private/ — the old
#    script verified this by hashing; here it cannot differ.
#
# The local mirror checkout (../oahu-electricity-future) is no longer used
# by the sync; keep it for browsing or retire it.
#
# Usage: ./push_both.sh "commit subject for the clean repo"
set -uo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
MSG="${1:-Sync results and report from working repository}"
MIRROR_URL="git@github.com:mikejrob/oahu-electricity-future.git"
cd "$SRC"

# Hard gate: no push while a solved result violates a must-hold relation.
# Runs on the published basis (best refinement per cell), the same numbers
# the report and explorer read. The Aug 2026 fuel-alias bug was visible to
# this check for four days pre-push while it was only run by hand.
python3 sanity_check_results.py || {
  echo "ABORT: sanity_check_results.py found violations - fix before pushing"; exit 1; }
python3 explorer/check_app_invariants.py || {
  echo "ABORT: explorer invariant regressed - fix before pushing"; exit 1; }

git push origin main || { echo "origin push failed"; exit 1; }

git remote get-url mirror >/dev/null 2>&1 || git remote add mirror "$MIRROR_URL"
git fetch mirror main --quiet || { echo "mirror fetch failed"; exit 1; }

# Guard: web edits on the mirror not yet absorbed. refs/mirror-synced marks
# the last mirror commit this script produced; anything beyond it on GitHub
# is a user directive that must be ported before a new snapshot lands.
if git rev-parse -q --verify refs/mirror-synced >/dev/null; then
  BEHIND=$(git rev-list --count refs/mirror-synced..refs/remotes/mirror/main)
  if [ "$BEHIND" -gt 0 ]; then
    echo "ABORT: mirror has $BEHIND commit(s) this script did not produce —"
    echo "user edits on GitHub. Port them into the working repo, then run:"
    echo "  git update-ref refs/mirror-synced refs/remotes/mirror/main"
    git log --oneline refs/mirror-synced..refs/remotes/mirror/main | sed 's/^/  unported: /'
    exit 1
  fi
fi

# Paths stripped from the public mirror. private/ never syncs. The
# holdback list below is TEMPORARY — delete a line to publish that path
# on the next push.
STRIP_PATHS=(private)
# HOLDBACK (2026-08-20, per author): talk decks stay off the mirror until
# the wheeling proposal is public. make_slides.sh goes with them so the
# mirror carries no build script for files it does not have.
STRIP_PATHS+=(slides build/make_slides.sh)

SRC_HEAD=$(git rev-parse HEAD)
TMPIDX=$(mktemp)
trap 'rm -f "$TMPIDX"' EXIT
STRIPPED=$(GIT_INDEX_FILE="$TMPIDX" git read-tree "$SRC_HEAD" \
  && GIT_INDEX_FILE="$TMPIDX" git rm -rf --cached -q --ignore-unmatch "${STRIP_PATHS[@]}" \
  && GIT_INDEX_FILE="$TMPIDX" git write-tree)

PARENT=$(git rev-parse refs/remotes/mirror/main)
if [ "$(git rev-parse "$PARENT^{tree}")" = "$STRIPPED" ]; then
  echo "clean repo already up to date at $(git rev-parse --short "$PARENT")"
  git update-ref refs/mirror-synced "$PARENT"
  exit 0
fi
NEW=$(git commit-tree "$STRIPPED" -p "$PARENT" -m "$MSG")
git push mirror "$NEW":refs/heads/main || { echo "clean push failed"; exit 1; }
git update-ref refs/mirror-synced "$NEW"
echo "clean repo pushed: $(git rev-parse --short "$NEW") (tree $STRIPPED)"
