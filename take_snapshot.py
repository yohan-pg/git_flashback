from git import Repo, IndexFile, Commit, Tree
from datetime import datetime
import pygit2

def create_label():
    return str(datetime.now()).replace(" ", "|").replace(".", ",").replace(":", ".")

repo = pygit2.Repository(".")
init_tree = repo.index.write_tree()

Tree.new(repo, "HEAD")
# Commit.create_from_tree(repo, IndexFile(repo), "")
# repo.index.write()

# index = IndexFile.from_tree(repo, "HEAD")
# repo.create_tag(create_label(), repo.head.target, 0, signature, "")