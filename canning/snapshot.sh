#!/bin/bash

LABEL=can/$(date +%Y-%m-%d/%H.%M.%S)
# taken from: https://stackoverflow.com/questions/48856649/make-a-snapshot-of-working-directory-with-git

INIT_TREE=$(git write-tree)
git add . 
git tag "$LABEL" "$(git commit-tree "$(git write-tree)" -p @ -m "worktree snap")"
git read-tree "$INIT_TREE"
echo "$LABEL"
