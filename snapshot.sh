#!/bin/bash

# lifted from: https://stackoverflow.com/questions/48856649/make-a-snapshot-of-working-directory-with-git

INIT_TREE=$(git write-tree)
STASHED_INDEX=$(git commit-tree -p @ -m "index snap" "$INIT_TREE")
git add -f .
TAG=salt/$(date +%Y-%m-%d/%H.%M.%S)
git tag "$TAG" "$(git commit-tree -p @ -p "$STASHED_INDEX" -m "worktree snap" "$(git write-tree)")"
git read-tree "$INIT_TREE"
echo "$TAG"