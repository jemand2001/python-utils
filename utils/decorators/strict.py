"""!
Adds strict type checking based on a function's annotations
"""
from inspect import signature, Parameter
from functools import wraps
from typing import Any, Callable

from utils.types_.is_instance import is_instance

__all__ = ["strict", "is_empty"]

## @cond
EMPTY = Parameter.empty
## @endcond


def is_empty(annotation) -> bool:
    """!
    Checks whether an annotation is empty
    @param annotation a Parameter.annotation
    @return whether the annotation is empty or not
    """
    return annotation in {EMPTY, Any}


def strict(f: Callable):
    """!
    Turns strict type checking on for the function
    @param f the decorated function
    """
    sig = signature(f)

    @wraps(f)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        for k, v in bound.arguments.items():
            par = sig.parameters[k]
            if not is_empty(par.annotation) and not is_instance(v, par.annotation):
                raise TypeError(
                    f"parameter {k} has invalid type: expected: {par.annotation} but got: {type(v)}"
                )
        res = f(*args, **kwargs)
        if not is_empty(sig.return_annotation) and not is_instance(
            res, sig.return_annotation
        ):
            raise TypeError(
                f"function '{f.__name__}' returned an unexpected"
                f" value: expected: {sig.return_annotation} but was: {type(res)}"
            )
        return res

    return wrapper
