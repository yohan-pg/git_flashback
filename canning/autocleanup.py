from .prelude import *

from .utils import *
from .snapshot import *

import atexit

__all__ = ["disable_autocleanup"]


autocleanup_enabled = True


def disable_autocleanup():
    global autocleanup_enabled
    autocleanup_enabled = False


@atexit.register
def cleanup():
    if autocleanup_enabled:
        os.system(f"git tag -d " + snapshot_label())