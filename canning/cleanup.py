from .prelude import *

from .utils import *
from .snapshot import *

import atexit

__all__ = ["disable_cleanup"]


save_was_used = False


def disable_cleanup():
    global save_was_used
    save_was_used = True


@atexit.register
def cleanup():
    if not save_was_used:
        os.system(f"git tag -d " + snapshot_tag())