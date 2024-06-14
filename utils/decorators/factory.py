"""!
This module contains a factory decorator.
"""
from functools import wraps
from inspect import signature, Parameter
from typing import Callable, Any

__all__ = "param_factory"


def param_factory(name: str, factory: Callable[[], Any]):
    """!
    Add a factory for a parameter of the decorated function

    ## Example usage:
    ```py
    @param_factory('test', lambda: 5)
    def mul2(test: int) -> int:
        return test * 2

    print(mul2(10))  # -> 20
    print(mul2())    # -> 10
    ```

    @param name the name of the parameter to add a factory to
    @param factory the factory to produce values for the parameter
    """

    def decorator(f: Callable):
        sig = signature(f)

        if name not in sig.parameters and not any(
            t == Parameter.VAR_KEYWORD for t in sig.parameters.values()
        ):
            raise TypeError(
                "Can't add a factory for a parameter that doesn't exist without **kwargs"
            )

        if sig.parameters[name].kind == Parameter.POSITIONAL_ONLY:
            raise TypeError("Can't add a factory for a positional-only parameter")

        @wraps(f)
        def inner(*args, **kwargs):
            bound = sig.bind_partial(*args, **kwargs)
            rest = {name: factory()} if name not in bound.arguments else {}
            return f(*bound.args, **bound.kwargs, **rest)

        return inner

    return decorator
