"""
When no save_fns are provided, we will default to pickle unless the 
object is a torch nn.Module, in which case we will use torch's save/load.
"""


from .prelude import *


def select_save_fn(obj: Any) -> bool:
    if "torch" in sys.modules:
        import torch

        if isinstance(obj, torch.nn.Module):
            if "dill" in sys.modules:
                import dill

                return lambda *args, **kwargs: torch.save(*args, **kwargs, pickle_module=dill)
            else:
                return torch.save

    if "dill" in sys.modules:
        import dill

        return dill.dump
    else:
        return pickle.dump


def select_load_fn() -> bool:
    if "torch" in sys.modules:
        import torch

        return torch.load
    
    if "dill" in sys.modules:
        import dill

        return lambda *args, **kwargs: torch.load(*args, **kwargs, pickle_module=dill)
    else:
        return pickle.load
