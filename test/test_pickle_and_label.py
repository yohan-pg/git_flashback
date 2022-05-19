import pickle_and_label as pal
import pickle

import sys
import shutil
import importlib


# * In these tests, copy2 is required modify metadata & avoid caching bugs.
# * I believe the caching error is OS-side, but I'm not sure.


def _import_or_reload(path):
    if path in sys.modules:
        del sys.modules[path]
    return importlib.import_module("tmp.example")


def test_restoration():
    shutil.copy2("test/fixtures/before.py", "tmp/example.py")
    label = pal.take_snapshot()
    pal.enable_load_from_git()

    module = _import_or_reload("tmp.example")
    assert module.Example().f() == 1
    pickle.dump(module.Example(), open(f"tmp/example.{label}.pkl", "wb"))

    shutil.copy2("test/fixtures/after.py", "tmp/example.py")
    module = _import_or_reload("tmp.example")
    assert module.Example().f() == 2
    
    assert pickle.load(open(f"tmp/example.{label}.pkl", "rb")).f() == 1
