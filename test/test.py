import pickle_and_label

import sys
import shutil
import importlib


before_path = "test/fixtures/before.py"
after_path = "test/fixtures/after.py"
module_path = "tmp/example.py"
pickle_path = "tmp/example.pkl"
module_dotpath = "tmp.example"


# * In these tests, copy2 is required modify metadata & avoid caching bugs.
# * I believe the caching error is OS-side, but I'm not sure.


def _import_or_reload(path):
    if path in sys.modules:
        del sys.modules[path]
    return importlib.import_module(module_dotpath)


def test_restoration():
    shutil.copy2(before_path, module_path)
    pickle_and_label.take_snapshot()

    module = _import_or_reload(module_dotpath)
    assert module.Example().f() == 1
    pickle_and_label.save(module.Example(), pickle_path)

    shutil.copy2(after_path, module_path)
    module = _import_or_reload(module_dotpath)
    assert module.Example().f() == 2
    assert pickle_and_label.load(pickle_path).f() == 1
