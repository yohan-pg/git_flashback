from .prelude import *

from .utils import *


def take_snapshot() -> None:
    if not hasattr(os.environ, SNAPSHOT_NAME_ENV_VAR):
        os.environ[SNAPSHOT_NAME_ENV_VAR] = bash(f"bash {DIR_PATH}/snapshot.sh")


def snapshot_tag() -> str:
    return os.environ[SNAPSHOT_NAME_ENV_VAR]


def write_snapshot_tag(file) -> str:
    return file.write(snapshot_tag().encode(TAG_ENCODING))


def read_snapshot_tag(file) -> str:
    return str(file.read(SNAPSHOT_NAME_LENGTH), TAG_ENCODING)


def git_current_tag() -> bool:
    return bash("git describe --tags")

