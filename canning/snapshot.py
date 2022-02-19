from .prelude import *

from .utils import *

# todo rename to timestamp?

def take_snapshot() -> None:
    os.environ[CANNING_TIMESTAMP_ENV_VAR] = bash(f"bash {DIR_PATH}/snapshot.sh")


def snapshot_label() -> str:
    return os.environ[CANNING_TIMESTAMP_ENV_VAR]


def git_head_matches_label(label: str) -> bool:
    return bash("git describe --tags --always") == label

