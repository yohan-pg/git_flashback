"""
When no save_fns are provided, we will default to pickle unless the 
object is a torch nn.Module, in which case we will use torch's save/load.
"""


from .prelude import *


def select_save_fn(obj: Any) -> bool:
    if "torch" in sys.modules:
        import torch

        if isinstance(obj, torch.nn.Module):
            return torch.save
    return pickle.dump


def select_load_fn() -> bool:
    if "torch" in sys.modules:
        import torch

        return torch.load
    return pickle.load
