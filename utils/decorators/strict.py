from inspect import signature, Parameter
from functools import wraps
from typing import Any

__all__ = ['strict']

EMPTY = Parameter.empty
def is_empty(annotation):
    return annotation in {EMPTY, Any}

def strict(f):
    sig = signature(f)

    @wraps(f)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        for k, v in bound.arguments.items():
            par = sig.parameters[k]
            if not is_empty(par.annotation) and not isinstance(v, par.annotation):
                raise TypeError(f"parameter {k} has invalid type: expected: {par.annotation} but got: {type(v)}")
        res = f(*args, **kwargs)
        if not is_empty(sig.return_annotation) and not isinstance(res, sig.return_annotation):
            raise TypeError(f"function '{f.__name__}' returned an unexpected"
                            f" value: expected: {sig.return_annotation} but was: {type(res)}")

    return wrapper
