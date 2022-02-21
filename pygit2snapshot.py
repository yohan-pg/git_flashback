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
