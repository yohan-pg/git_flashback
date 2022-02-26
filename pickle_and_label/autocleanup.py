from .prelude import *

from .utils import *
from .label import *

import atexit


__all__ = ["enable_autocleanup", "disable_autocleanup"]

autocleanup_enabled = False


def enable_autocleanup():
    global autocleanup_enabled
    autocleanup_enabled = True


def disable_autocleanup():
    global autocleanup_enabled
    autocleanup_enabled = False


@atexit.register
def cleanup():
    if autocleanup_enabled:
        repo.references.delete(repo.revparse_ext(snapshot_label())[1].name)