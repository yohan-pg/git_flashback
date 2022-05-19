from git_flashback import * 

import pickle
import sys
import shutil
import importlib
import time
import os 

class setup_tmp_dir:
    shutil.rmtree("tmp", ignore_errors=True)
    os.mkdir("tmp")
    open("tmp/__init__.py", "w").close() #! This should not be required (bug)
    shutil.copy("tests/fixtures/before.py", "tmp/example.py")


def _load_or_reload(module_path: str):
    os.system("rm -r tmp/__pycache__") #! I don't understand why this is required, but it is
    if module_path in sys.modules:
        del sys.modules[module_path]
    return importlib.import_module(module_path)


def _load_example_module():
    shutil.copy("tests/fixtures/before.py", "tmp/example.py")
    return _load_or_reload("tmp.example")


def _load_example_module_after_changes():
    shutil.copy("tests/fixtures/after.py", "tmp/example.py")
    return _load_or_reload("tmp.example")


def test_restoration():
    """
    Modify your code without fear. Later, flashback to the old codebase when loading your objects. This transparently loads the required modules from your snapshot, rather than the modified ones in your current filesystem.
    """
    module = _load_example_module()
    assert module.Example().f() == 1

    timestamp = snapshot()
    pickle.dump(module.Example(), open(f"tmp/{timestamp}.pkl", "wb"))

    module = _load_example_module_after_changes()
    assert module.Example().f() == 2
    
    with flashback(timestamp):
        assert pickle.load(open(f"tmp/{timestamp}.pkl", "rb")).f() == 1


def test_tags_made_in_the_same_second_are_shared():
    pass




def test_paths_are_ignored_in_timestamps():
    """
    For conveniance, flashback will ignore everything before the rightmost forward slash, so a path like "experiments/20220519T150016.264685" can be passed directly to it.
    """
    timestamp = snapshot()

    with flashback("any_path/" + timestamp):
        pass


def test_timestamp_matches():
    """
    When attempting to load from a timestamp which matches the current HEAD, snapshot will return the current tag (doing nothing) and flashback will instead load from the present (does nothing also).
    """


def test_code_editing():
    pass


def test_flashback_to_commit():
    pass


def test_isinstance():
    pass

def test_issubclass():
    pass



# - test: paths work when running from another directory
# - test: torch compatibiltiy
# - test: repo.index.add_all() reflects what the user adds manually to the index 
#       (this will be tricky to test! maybe just do it manually)
