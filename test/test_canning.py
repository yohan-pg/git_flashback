import sys
import shutil
import importlib
import canning


before_path = "test/fixtures/before.py"
after_path = "test/fixtures/after.py"
module_path = "tmp/example.py"
can_path = "tmp/example.can"
module_dotpath = "tmp.example"

# * In these tests, copy2 is required modify metadata & avoid caching bugs.
# * I beleive the caching error is OS-side but I'm not sure


def _import_or_reload(path):
    if path in sys.modules:
        del sys.modules[path]
    return importlib.import_module(module_dotpath)


def test_restoration():
    shutil.copy2(before_path, module_path)
    canning.take_snapshot()

    module = _import_or_reload(module_dotpath)
    assert module.Example().f() == 1
    canning.save(module.Example(), can_path)

    shutil.copy2(after_path, module_path)
    module = _import_or_reload(module_dotpath)
    assert module.Example().f() == 2
    assert canning.load(can_path).f() == 1
