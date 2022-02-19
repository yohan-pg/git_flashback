from .prelude import *


def file_extension_is_valid(filename: str) -> bool:
    return filename.split(".")[-1] == "can"


def bash(cmd):
    return os.popen(cmd).read().strip()
