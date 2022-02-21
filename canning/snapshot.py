from .prelude import *

from .utils import *

# todo rename to timestamp?


def take_snapshot() -> None:
    # TODO avoid bash
    os.environ[CANNING_TIMESTAMP_ENV_VAR] = bash(f"bash {DIR_PATH}/snapshot.sh")


def snapshot_label() -> str:
    return os.environ[CANNING_TIMESTAMP_ENV_VAR]


def git_head_matches_label(label: str) -> bool:
    # TODO avoid bash
    return (
        repo.describe(
            describe_strategy=pygit2.GIT_DESCRIBE_TAGS, show_commit_oid_as_fallback=True
        )
        == label
    )
