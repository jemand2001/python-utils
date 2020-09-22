from inspect import signature, Parameter
from functools import wraps


__all__ = ['strict', 'all_args']
EMPTY = Parameter.empty


def all_args(*args, **kwargs):
    return args + tuple(kwargs.values())


def strict(f):
    sig = signature(f)
    @wraps(f)
    def wrapper(*args, **kwargs):
        for par, arg in zip(sig.parameters.values(), all_args(*args, **kwargs)):
            if par.annotation is not par.empty and not isinstance(arg, par.annotation):
                raise TypeError(f"parameter '{par.name}' has invalid type: expected: {par.annotation} but was: {type(arg)}")
        res = f(*args, **kwargs)
        if sig.return_annotation is not EMPTY and not isinstance(res, sig.return_annotation):
            raise TypeError(f"function '{f.__name__}' returned an unexpected value: expected: {sig.return_annotation} but was: {type(res)}")
        return res
    return wrapper
