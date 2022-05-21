import sys
INIT_MODULES = sys.modules.copy()

import pygit2
from typing import * # type: ignore
from types import ModuleType
from io import BufferedWriter
import sys
import os

REPO = pygit2.Repository(".") 

