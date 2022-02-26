from .prelude import *

from .utils import *

from .autocleanup import *
from .label import *

from datetime import datetime


def take_snapshot() -> None:
    init_tree = repo.index.write_tree()
    label = create_label()
    try:
        signature = repo.get(repo.head.target).author
    except pygit2.GitError:
        raise Exception("Your current repository has no commits! Please commit something first.")
    # * Note that .write() is never called, so this doesn't modify the user-facing index
    repo.index.add_all()
    commit_hash = repo.create_commit(
        None,
        signature,
        signature,
        label,
        repo.index.write_tree(),
        [repo.head.target],
    )
    repo.create_tag(
        label,
        commit_hash,
        pygit2.GIT_OBJ_COMMIT,
        signature,
        "~Canning snapshot~",
    )
    repo.index.read_tree(init_tree)
    os.environ[CANNING_SNAPSHOT_ENV_VAR] = label
    enable_autocleanup()

