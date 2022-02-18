from gitimport import modules_from_git
import pickle 
import pygit2
import os
import sys
import atexit

# todo add an option to tolerate missing commits 
# todo patch subclasscheck
# todo if the current commit matches the snapshot, just load form the current working directory
# todo pickle interface -> use torch
# todo avoid heavy snapshots by imposing a file limit
# todo verbose mode for deleted tags
# todo unit test this
# todo snapshot with pygit2

SNAPSHOT_NAME_LENGTH = 24

def bash(cmd):
    os.popen(cmd).read().strip()

if not hasattr(os.environ, "SALT_SNAPSHOT"):
    os.environ["SALT_SNAPSHOT"] = bash("bash snapshot.sh")

save_was_called = False

def save(obj, filename: str, enforce_correct_extension: bool = True) -> None:
    global save_was_called 
    save_was_called = True

    if enforce_correct_extension:
        assert filename.split(".")[-1] == "salt"
    
    with open(filename, "wb") as file:
        file.write(os.environ["SALT_SNAPSHOT"].encode("ascii"))
        pickle.dump(obj, file)

def load(filename: str, enforce_correct_extension: bool = True):
    if enforce_correct_extension:
        assert filename.split(".")[-1] == "salt"
    
    with open(filename, "rb") as file:
        if inside_the_snapshot():
            return pickle.load(file)
        else:
            with modules_from_git(str(file.read(SNAPSHOT_NAME_LENGTH), "ascii")):
                return pickle.load(file)

def inside_the_snapshot() -> bool:
    current_branch = bash("git rev-parse --abbrev-ref HEAD")
    return current_branch == os.environ["SALT_SNAPSHOT"]

@atexit.register
def cleanup():
    if not save_was_called:
        os.system(f"git tag -d " + os.environ["SALT_SNAPSHOT"])

from a import Cls

# save(Cls(), "cls.salt")
cls = load("cls.salt")

print(cls.f())
