"""!
Adds the ability to overload functions
"""
from inspect import signature, Signature
from collections import defaultdict
from functools import wraps
from typing import Callable, MutableMapping
from types import FunctionType
from .strict import is_empty


__all__ = ["overload"]


overloaded: MutableMapping[str, MutableMapping[Signature, Callable]] = defaultdict(dict)


## @cond
def to_string(args, kwargs) -> str:
    return (
        "("
        + ", ".join(
            (
                ", ".join(map(repr, args)),
                ", ".join(f"{k}={v}" for k, v in kwargs.items()),
            )
        )
        + ")"
    )


## @endcond


def overload(f: FunctionType):
    """!
    The overload decorator

    This decorator allows you to write separate implementations for a function based on the arguments provided.
    To use it, just annotate your function's implementations with the types they expect.

    Keep in mind that all implementations need to be decorated with `@overload` to be considered.
    If there are multiple implementations for the same signature and annotations, only the last one is considered.

    ## Example:
    ```py
    @overload
    def f(x: int):
        print('x is an int')

    @overload
    def f(x: str):
        print('x is a string')

    f(12)  # prints "x is an int"
    f('test')  # prints "x is a string"
    f(1.2)  # raises a TypeError('No overloads for f with arguments: (1.2, )')
    ```

    @param f the overloaded function
    """
    name = f"{f.__module__}.{f.__qualname__}"
    overloaded[name][signature(f)] = f

    @wraps(f)
    def wrapper(*args, **kwargs):
        to_call = None
        for sig, func in overloaded[name].items():
            try:
                arguments = sig.bind(*args, **kwargs)
                if all(
                    is_empty(sig.parameters[k].annotation)
                    or isinstance(v, sig.parameters[k].annotation)
                    for k, v in arguments.arguments.items()
                ):
                    to_call = func
                    return to_call(*args, **kwargs)
            except TypeError:
                continue
        if to_call is None:
            raise ValueError(
                f"No overloads for {name} with arguments: {to_string(args, kwargs)}"
            )

    return wrapper
