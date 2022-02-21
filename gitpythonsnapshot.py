repo = Repo(".")
assert not repo.bare
repo.create_tag(create_label())