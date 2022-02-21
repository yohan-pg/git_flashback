from gitimport import modules_from_git

import pickle
import pygit2
import os
import sys
from typing import *
from types import ModuleType
from io import BufferedWriter

repo = pygit2.Repository(".") # TODO set this from an env var?
signature = pygit2.Signature("canning", "can@can.com")

LoadedObject = TypeVar("LoadedObject")
SaveFn = Callable[[Any, Any], None]
LoadFn = Callable[[Any], None]

CANNING_SNAPSHOT_ENV_VAR = "CANNING_TIMESTAMP"
TEXT_ENCODING = "ascii"
MAGIC_NUMBER = "CAN"
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
