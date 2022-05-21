A work in progress
# `git_flashback`

`git_flashback` is a Python library which lets you **load modules from the past** and thus **unpickle objects from the past**, by remembering their source code with git.

This is implemented with *transparent git snapshots* (which commit and tag your codebase, without affecting your working directory), and *transparent module loading* (which loads source code directly from within the git filesystem, without affecting your working directory).

The intended use case is reproductible machine learning experiments. But, `git_flashback` is agnositic to external libraries such as torch, and can be used as a generic tool for temporarily restoring code to its older versions.

## Example 1: unpickling from the past

First, call `snapshot` to (transparently) commit and tag your codebase. You can then pickle your objects normally. 

```python
import git_flashback import snapshot

timestamp = snapshot()
print(timestamp) # => 20220519T150016

import torch 

class Model(torch.nn.Module):
    def forward(self):
        return 1

torch.save(Model(), f"model.pt") # works with torch, pickle, dill, or anything else

# Figure 1: `snapshot` commits your code in the background and tags it with a timestamp
```

Modify your code without fear. Later, `flashback` to the old codebase when loading your objects. This transparently loads their source code from your git snapshot, rather than the modified code in your current filesystem.

```python
import git_flashback import flashback
import torch

class Model(torch.nn.Module):
    def forward(self):
        return 2

with flashback("20220519T150016"): 
    model = torch.load("model.pt")

print(model()) # => 1

# Figure 2: `flashback` rewires imports so that modules and unpickled objects load from the past
```

Regardless of your code changes (your package structure), `model` will behave *exactly as when saved*. 

> Timestamps like *20220519T150016* are [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) *basic format* timestamps, which are used instead of the *extended format* like 2022-05-19T15:00:16.264685 because git does not support semicolons in tags.


### Workflow tips
It is recommended to snapshot as soon as possible, before the rest of your imports. This is to avoid delays in producing the snapshot, and because modules loaded before `git_flashback` will not be modified during a flashback.

```python
import git_flashback import snapshot
timestamp = snapshot()

# all imports go right below
import torch
import csv 
import os

...

# Figure 3: `snapshot` should be called before imports
```

A nice way of working is to save all artifacts in a directory named with the timestamp (this is a natural way of bundling the timestamp alongside the saved objects).

```python
...

os.mkdir(f"experiments/{timestamp}")
torch.save(f"experiments/{timestamp}/model.pt")

# Figure 4: save the timestamp alongside artifacts, for instance, by naming their directory
```

For conveniance, `flashback` will ignore everything before the rightmost forward slash, so a path like `"experiments/20220519T150016"` can be passed directly to it.

```python
with flashback("experiments/20220519T150016"): 
    # loads the snapshot "20220519T150016"
    ... 
```

### Back to the future (past code editing)
Timestamps are just git tags, and can be checked out, letting you inspect and debug your past experiments.

```bash 
git checkout 20220519T150016
```

<!-- todo but snapshot doesn't know we are aiming for 20220519T150016 -->
**When attempting to load from a timestamp which matches the current `HEAD`, `flashback` will instead load from the present.**
For example, after the checkout, the following code unpickles from the present, because the timestamp matches:

```python
# currently in commit tagged '20220519T150016'

class Model(torch.nn.Module):
    def forward(self):
        return 3 # edited

with flashback("20220519T150016"): 
    # loads from the present
    model = torch.load("model.pt") 
    
print(model()) # => 3

# Figure 5: when a past snapshot is checked out, `snapshot` and `flashback` are no-ops
```

This is a bit hard to see in a contrived example, but this makes it easy to checkout a past snapshot, edit its code, and verify that the changes work as desired. Afterwards, they can be committed normally:

```bash
git add .
git commit -m "Modified experiment 20220519T150016"
# => 4a2a14084b044d90f892f6201dd89dadc36db7a5
git checkout main
```

Additionally, it is possible to flashback to commits directly, letting us use the changed code while sitting comfortably in `main`:

```python
# currently in `main`

with flashback("4a2a14084b044d90f892f6201dd89dadc36db7a5"): 
    model = torch.load("model.pt")

print(model()) # => 3

# Figure 6: from `main`, loading a modified version of the past 
```


## Example 2: compring past modules

When debugging or after peforming refactors, it is often desirable to compare the new code's behavior to its older versions. `git_flashback` provides a conveniant way of doing so, by loading code from past snapshots or commits.

```python
from git_flashback import flashback
import my_module

# `flashback` to an older commit; any git revision is valid!
with flashback("fcfee1d161cd4dd9e07af841b1166dbbd8a07980"): 
    import my_module as my_old_module

assert my_module.f() == my_old_module.f()

# Figure 7: compare two different versions of the same module
```

It is important to note that everything is duplicated, including the class definitions but also the subdependencies themselves. This means that any state modification will be remain isolated within each module.


## Sharing snapshots
To share snapshots, simply push their tags to github. 

```bash
# first host
git push origin 20220519T150016
```

Then, on your other host, make sure to fetch them before calling `flashback`.

```bash
# second host
git fetch
```

## Cleaning up old snapshots

Because snapshots are just diffs, they are very lightweight, provided that `gitignore` is configured properly to ignore large artifacts. Still, it may be desirable to avoid clutter by deleting old snapshots. To do so, just remove their tags from git, leaving them to be garbage collected. For instance, if all tags are saved as subdirectories of `experiments/`, the following command clears out all the other ones:

```bash
comm -23 <(git tag -l) <(ls experiments/) | xargs -n 1 git tag -d
```

<!-- todo this also removes other tags. need to filter based on comment -->

## Caveats

### Typing and class duplication
Because objects loaded from the past do not have the same class definitions, `isinstance` and `issubclass` will return `False` when compared to classes from the present (which is technically true, but may be undesirable).

For this reason, `git_flashback` exports the following functions:
- `isinstance_by_name` and `issubclass_by_name`, which considers classes to be equal if they have the same name.
- `isinstance_by_qualname` and `issubclass_by_qualname`, which considers classes to be equal if they have the same name *and packaging path* (qualname).

Of course, it is also possible to manually override `__instancecheck__` and `__subclasscheck__` on your classes to implement any desired behavior.

### Dynamic imports
Python does not support loading multiple versions of the same dependencies by default. So, this library works by clearing out
`sys.modules`, repopulating it with old code, and finally restoring it back to what is was. **As such, any dynamic imports of uncached modules in past code will look at new code.** To avoid this, avoid dynamic imports.


## Acknowledgements
This library is a small wrapper around [gitimport](https://pypi.org/project/gitimport/), which carries most of the implementation weight. :)  


<!-- todo explain the implementation briefly -->