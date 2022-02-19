from .prelude import *

from .utils import *
from .fn_selection import *
from .autocleanup import *
from .snapshot import *
from .can import *


Target = Union[str, BufferedWriter]


def save(
    obj: Any,
    target: Target,
    save_fn: Callable = None,
) -> None:
    if save_fn is None:
        save_fn = select_save_fn(obj)

    with target_to_file(target, "wb") as file:
        Can(file).write_with(save_fn, obj)

    disable_autocleanup()


def load(target: Target, load_fn: SaveFn = None, snapshot: str = None) -> LoadedObject:
    return load_with_modules(target, load_fn, snapshot=snapshot)[0]


def load_with_modules(
    target: Target, load_fn: LoadFn = None, snapshot: str = None
) -> Tuple[LoadedObject, Dict[str, ModuleType]]:
    if load_fn is None:
        load_fn = select_load_fn()

    with target_to_file(target, "rb") as file:
        return Can(file).read_with(load_fn, snapshot=snapshot)


def target_to_file(target: Target, flag: str):
    if isinstance(target, str):
        assert file_extension_is_valid(target)
        return open(target, flag)
    else:
        # todo assert flag is OK
        assert False
        return target
