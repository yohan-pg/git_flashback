# The MIT License (MIT)

# Copyright (c) 2015 Matthias Bartelmeß

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ----------------------------------------------------------------------

# This is a simplified version of `gitimport` by Matthias Bartelmeß
# https://github.com/fourplusone/gitimport

import pygit2
import os.path
from importlib.machinery import ModuleSpec
from importlib.abc import PathEntryFinder, Loader
import contextlib
import sys
from typing import Optional
from .errors import *


BasePath = str  # A path which ends in a .git/ folder, example: /Users/Yohan/Desktop/Projects/git_flashback/.git/
SHA = str  # A git object hash, example: 8902274b0380ba35df3985bdcb9c342c792befb2


"""
Here is a breif overview of how the import system is used:

When path is imported, the callables in `sys.path_hooks` are called with it. The first one that returns a finder object successfully (without raising ImportError) is used.

# todo: different between `path` and `modulename`


"""


GIT_PATH_SYMBOL = "+git+"


class GitFinder(PathEntryFinder):
    def __init__(self, path: str):
        self.path = path

        if GIT_PATH_SYMBOL not in path:
            raise ImportError()

        self.repo_basepath, self.sha = path.split(GIT_PATH_SYMBOL, 1)
        self.repo: pygit2.Repository = pygit2.Repository(self.repo_basepath)

        try:
            self.commit: pygit2.Commit = self._resolve_commit(self.sha)
        except:
            raise ImportError()

    def find_spec(self, modulename: str, target):  # ?? what is target
        if spec := self._search_for_spec(modulename, ".py"):
            return spec
        elif spec := self._search_for_spec(modulename, "/__init__.py"):
            spec.submodule_search_locations = [os.path.join(self.path, "/__init__.py")]
            return spec
        else:
            return None

    def _search_for_spec(self, modulename, extension: str) -> Optional[ModuleSpec]:
        tail_modulename = modulename.rpartition(".")[2]
        breakpoint()
        try:
            tree_entry = self.commit.tree[tail_modulename + extension]  # type: ignore
        except KeyError:
            pass
        else:
            if isinstance(tree_entry, pygit2.Blob):
                return ModuleSpec(
                    modulename,
                    GitLoader(tree_entry, self.repo, self.sha),
                    origin=tail_modulename + extension,
                )

        return None

    # todo can we avoid this function?
    def _resolve_commit(self, reference: str) -> pygit2.Commit:
        object = self.repo.get(reference)

        while isinstance(object, pygit2.Tag):
            object = self.repo.get(object.target)

        return object  # type: ignore


class GitLoader(Loader):
    def __init__(self, tree_entry: pygit2.Tree, repo: pygit2.Repository, sha: Optional[str] = None):
        self.tree_entry = tree_entry
        self.repo = repo
        self.sha = sha

    def get_code(self):
        return self.repo[self.tree_entry.id].data  # type: ignore

    def exec_module(self, module):
        if self.sha is not None:
            module.__git_commit__ = self.sha  # type: ignore
        exec(self.get_code(), module.__dict__)


def add_gitimport_hook(repo: pygit2.Repository, revision: str = "HEAD") -> str:
    if GitFinder not in sys.path_hooks:
        sys.path_hooks.append(GitFinder)

    path = f"{repo.path}{GIT_PATH_SYMBOL}{repo.revparse_single(revision).hex}"
    sys.path.insert(0, path)

    return path


def remove_gitimport_hook(path: str):
    sys.path.remove(path)
    sys.path_hooks.remove(GitFinder)
