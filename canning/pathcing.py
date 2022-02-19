

def compatible_across_versions(cls):
    class Uncanned(cls):
        def __issubclass__(cls, other):
            return cls.__name__ == other.__name__ or issubclass(other, cls) 

        def __instancecheck__(cls, inst):
            return inst.__class__.__name__ == cls.__name__ or isinstance(inst, cls) 
    
    Uncanned.__name__ = "Uncanned" + cls.__name__
    return Uncanned

# @canning.compatible_across_versions  