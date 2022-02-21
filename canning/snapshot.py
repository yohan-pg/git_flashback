from .prelude import *

from .utils import *

from datetime import datetime


def take_snapshot() -> None:
    init_tree = repo.index.write_tree()
    label = create_label()
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
        label,
    )
    repo.index.read_tree(init_tree)
    os.environ[CANNING_SNAPSHOT_ENV_VAR] = label


def snapshot_label() -> str:
    # todo give this function a better name
    return os.environ[
        CANNING_SNAPSHOT_ENV_VAR
    ]  # todo give the env var a better name also


def git_head_matches_label(label: str) -> bool:
    return (
        repo.describe(
            describe_strategy=pygit2.GIT_DESCRIBE_TAGS, show_commit_oid_as_fallback=True
        )
        == label
    )


def create_label() -> str:
    return str(datetime.now()).replace(" ", "/").replace(".", "/").replace(":", ".")
