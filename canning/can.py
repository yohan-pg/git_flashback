from .prelude import *
from .utils import *
from .snapshot import *


class Can:
    def __init__(self, file: BufferedWriter):
        self.file = file

    def write_with(self, save_fn: SaveFn, obj: Any) -> None:
        self.write_magic_number()
        self.write_label()
        save_fn(obj, self.file)

    def read_with(self, load_fn: LoadFn, snapshot: Optional[str] = None) -> Tuple[LoadedObject, Dict[str, ModuleType]]:
        assert self.read_magic_number() == MAGIC_NUMBER, "Invalid .can file"
        label = self.read_label()

        if snapshot is not None:
            label = snapshot
        
        if git_head_matches_label(label):
            return load_fn(self.file), sys.modules
        else:
            with modules_from_git(label) as modules:
                return load_fn(self.file), modules

    def write_magic_number(self) -> str:
        return self.file.write(MAGIC_NUMBER.encode(TEXT_ENCODING))

    def read_magic_number(self) -> str:
        return str(self.file.read(len(MAGIC_NUMBER)), TEXT_ENCODING)

    def write_label(self) -> str:
        return self.file.write(snapshot_label().encode(TEXT_ENCODING))

    def read_label(self) -> str:
        return str(self.file.read(SNAPSHOT_NAME_LENGTH), TEXT_ENCODING)
