from git import Repo, IndexFile, Commit, Tree
from datetime import datetime
import pygit2

signature = pygit2.Signature("canning", "can@can.com")

def create_label():
    return str(datetime.now()).replace(" ", "/").replace(".", "/").replace(":", ".")

repo = pygit2.Repository(".")
init_tree = repo.index.write_tree()
repo.index.add_all()

label = create_label()
commit_hash = repo.create_commit(
    "HEAD", 
    signature, 
    signature, 
    label, 
    repo.index.write_tree(), 
    [repo.head.target]
)
repo.create_tag(create_label(), commit_hash, 0, signature, "")