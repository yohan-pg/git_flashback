from .prelude import *

from .utils import *
from .fn_selection import *
from .cleanup import *
from .snapshot import *


Target = Union[str, BufferedWriter]


def save(
    obj: Any,
    target: Target,
    save_fn: Callable = None,
) -> None:
    if save_fn is None:
        save_fn = select_save_fn(obj)

    with target_to_file(target, "wb") as file:
        write_snapshot_tag(file)
        save_fn(obj, file)

    disable_cleanup()



def load(target: Target, load_fn: Callable = None, revision: str = None) -> LoadedObject:
    return load_with_modules(target, load_fn, revision=revision)[0]


def load_with_modules(
    target: Target, load_fn: Callable = None, revision: str = None
) -> Tuple[LoadedObject, Dict[str, ModuleType]]:
    if load_fn is None:
        load_fn = select_load_fn()

    with target_to_file(target, "rb") as file:
        tag = read_snapshot_tag(file) if revision is None else revision
        
        if git_current_tag() == tag:
            return load_fn(file), sys.modules
        else:
            with modules_from_git(tag) as modules:
                return load_fn(file), modules


def target_to_file(target: Target, flag: str):
    if isinstance(target, str):
        assert file_extension_is_valid(target)
        return open(target, flag)
    else:
        # todo assert flag is OK
        assert False
        return target
