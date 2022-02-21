#!/bin/bash
# Taken from: https://stackoverflow.com/questions/48856649/make-a-snapshot-of-working-directory-with-git

# Create a tree object from the current index, as a backup I think.
INIT_TREE=$(git write-tree)

# Add the entire working directory to the index & commit that
git add .
TIMESTAMP=can/"$(date +%Y-%m-%d/%H.%M.%S)"
git tag "$TIMESTAMP" "$(git commit-tree -p HEAD -m "can" "$(git write-tree)")"

# Restore the index from the backup
git read-tree "$INIT_TREE"

# 
echo "$TAG"

# past = repo.create_tag('past', ref=new_branch, message="This is a tag-object pointing to %s" % new_branch.name)
# Create new indices from other trees or as result of a merge. Write that result to a new index file for later inspection.
# from git import IndexFile
# # loads a tree into a temporary index, which exists just in memory
# IndexFile.from_tree(repo, 'HEAD~1')
# # merge two trees three-way into memory
# merge_index = IndexFile.from_tree(repo, 'HEAD~10', 'HEAD', repo.merge_base('HEAD~10', 'HEAD'))
# merge_index.write(os.path.join(rw_dir, 'merged_index'))

# todo creates a tag with pygit2
# repo.create_tag(create_label(), repo.head.target, 0, signature, "")
