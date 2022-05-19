from .prelude import *
from .save_load import *

import glob


def cleanup_snapshots(dir_path: str = "."):
    can_paths = glob.glob(f"{dir_path}/**/*.can", recursive=True)

    preserved_labels = []
    for can_path in can_paths:
        preserved_labels.append(read_label(can_path))

    for tag in [o for o in repo.references.objects if o.name.startswith("refs/tags/")]:
        if (
            repo.get(tag.target).message == COMMIT_COMMENT
            and tag.name not in preserved_labels
        ):
            repo.references.delete(tag.name)
