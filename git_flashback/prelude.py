from gitimport import modules_from_git

import pickle
import pygit2
import os
import sys
from typing import * # type: ignore
from types import ModuleType
from io import BufferedWriter

repo = pygit2.Repository(".") # TODO set this from an env var?

LoadedObject = TypeVar("LoadedObject")

SNAPSHOT_ENV_VAR = "GIT_SNAPSHOT_TIMESTAMP"
COMMIT_COMMENT = "GIT FLASHBACK SNAPSHOT"