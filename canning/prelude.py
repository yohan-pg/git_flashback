from gitimport import modules_from_git
import pickle
import pygit2
import os
import sys
from typing import *
from types import ModuleType
from io import BufferedWriter


LoadedObject = TypeVar("LoadedObject")

SNAPSHOT_NAME_LENGTH = 23
SNAPSHOT_NAME_ENV_VAR = "CAN_SNAPSHOT"
TAG_ENCODING = "ascii"
MAGIC_NUMBER = "CAN".encode(TAG_ENCODING)
DIR_PATH = os.path.dirname(os.path.realpath(__file__))