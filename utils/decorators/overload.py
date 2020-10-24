from inspect import signature, Parameter
from collections import defaultdict
import typing


__all__ = ['overload']


overloaded = defaultdict(dict)

def overload(f: typing.Callable):
    if any(par.kind in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD)):
        raise TypeError('cannot overload variable argument lists')
    overloaded[f.__name__][signature(f)] = f

    @wraps(f)
    def wrapper(*args, **kwargs):
        all_args = args + tuple(kwargs.values())
        for sig, func in overloaded[f.__name__].items():
            if len(all_args) == len(sig.parameters) and all(isinstance(arg, parameter.annotation) for parameter, arg in zip(sig.parameters.values(), all_args)):
                return func(*args, **kwargs)
    return wrapper
