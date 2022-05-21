"""

Useful reference: https://docs.python.org/3/library/importlib.html#approximating-importlib-import-module

"""

from .prelude import *

from .timestamp import *

import contextlib

from importlib.abc import MetaPathFinder, Loader
from importlib.machinery import ModuleSpec


def flashback(revision: str):
    assert isinstance(revision, str)

    # * Conveniance for when the revision taken from a folder name
    revision = revision.split("/")[-1]

    # if git_head_matches_timestamp(revision):
    #     return dummy_context_manager()
    # else:
    return load_modules_from_git(revision)


@contextlib.contextmanager
def dummy_context_manager():
    yield sys.modules


@contextlib.contextmanager
def load_modules_from_git(revision: str):
    def empty_out_modules() -> dict:
        saved_modules = sys.modules.copy()
        sys.modules.clear()
        sys.modules.update(INIT_MODULES)
        return saved_modules

    def repopulate_modules(saved_modules: dict, final_modules: dict):
        final_modules.update(sys.modules)
        sys.modules.clear()
        sys.modules.update(saved_modules)

    finder = GitFinder(revision)

    sys.meta_path.insert(0, finder)
    saved_modules = empty_out_modules()

    final_modules = {}
    yield final_modules

    repopulate_modules(saved_modules, final_modules)
    sys.meta_path.remove(finder)


class GitFinder(MetaPathFinder):
    def __init__(self, revision: str):
        self.commit: pygit2.Commit = self._resolve_commit(revision)

    def find_spec(
        self,
        fullname: str,
        path: Optional[Sequence[str]], #?
        target: Optional[ModuleType] = None,
    ) -> Optional[ModuleSpec]:
        if spec := self._search_for_spec(fullname, ".py"):
            return spec
        elif spec := self._search_for_spec(fullname, "/__init__.py"):
            spec.submodule_search_locations = [fullname] #!!! this is incorrect
            return spec
        elif spec := self._search_for_spec(fullname, ""):
            return spec
        else:
            raise ImportError(f"No module named {fullname}") #todo better error

    def _search_for_spec(self, modulename: str, extension: str) -> Optional[ModuleSpec]:
        origin = modulename.replace(".", "/") + extension #? why split
        try:
            tree = self.commit.tree[origin]  
        except KeyError:
            return
        else:
            if isinstance(tree, pygit2.Blob): # ? would it not be?
                return ModuleSpec(
                    modulename,
                    GitLoader(REPO[tree.id].data),
                    origin=origin,
                )

        return None

    # ? can we avoid this function?
    def _resolve_commit(self, revision: str) -> pygit2.Commit:
        object = REPO.revparse_single(revision)

        while isinstance(object, pygit2.Tag):
            object = REPO.get(object.target)

        return object # type: ignore


class GitLoader(Loader):
    def __init__(self, source_code: str):
        self.source_code = source_code

    # ? can we use something default insead?
    def exec_module(self, module):
        exec(self.source_code, module.__dict__)

    # todo create module fn is missing? 
