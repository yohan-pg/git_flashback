from .prelude import *


def file_extension_is_valid(filename: str) -> bool:
    return filename.split(".")[-1] == "can"

