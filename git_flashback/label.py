from .prelude import *

from datetime import datetime


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
    return datetime.now().isoformat().replace("-", "").replace(":", "")
