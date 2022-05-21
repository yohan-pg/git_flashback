"""
Implements transparent snapshotting (commit + tagging) of the current working directory.

Roughly, the current index is first saved.
Then, all files are added to the index, a new commit is created (which does not affect the index), and tagged with a timestamp.
Finally, the index is restored to its initial state, and the timestamp is returned.
"""

from .prelude import *

from .timestamp import *

import importlib

def snapshot() -> str:
    init_tree = REPO.index.write_tree() #??? what is this for again?
    timestamp = create_timestamp()

    try:
        signature = REPO.get(REPO.head.target).author # type: ignore
    except pygit2.GitError:
        raise Exception("Your current repository has no commits! Please commit something first.")
    
    # * Note that .write() is never called, so this doesn't modify the user-facing index
    REPO.index.add_all()
    commit_hash = REPO.create_commit(
        None,  # type: ignore
        signature,
        signature,
        timestamp,
        REPO.index.write_tree(),
        [REPO.head.target],
    )
    try:
        REPO.create_tag(
            timestamp,
            commit_hash,
            pygit2.GIT_OBJ_COMMIT,
            signature,
            "GIT FLASHBACK SNAPSHOT",
        )
    except pygit2.AlreadyExistsError:
        pass
    
    # todo if this is missing, can we damage our actual working index or is this an index within pygit2?
    REPO.index.read_tree(init_tree) 
    
    return timestamp

