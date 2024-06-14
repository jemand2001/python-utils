"""!
Contains a decorator that allows you to convert parameters to the decorated function using converter functions.
"""
from inspect import Signature, signature, Parameter, BoundArguments
from typing import Callable, TypeVar, Tuple, Union
from functools import wraps, WRAPPER_ASSIGNMENTS


__all__ = ["convert"]


## @cond
T = TypeVar("T")
## @endcond

def _convert_param(
    name: str, bound: BoundArguments, param: Parameter
) -> Union[T, Tuple[T]]:
    if isinstance(param.annotation, Callable) and param.annotation != Parameter.empty:
        func = param.annotation
    else:

        def func(x):
            return x

    if param.kind == Parameter.VAR_POSITIONAL:
        return (*map(func, bound.arguments[name]),)
    elif param.kind == Parameter.VAR_KEYWORD:
        return {k: func(v) for k, v in bound.arguments[name].items()}
    else:
        return func(bound.arguments[name])


def convert(f: Callable):
    """!
    The convert decorator.

    This decorator allows you to implicitly convert arguments to a function.
    It treats the parameter annotations as converters, if they're callable;
    otherwise it just passes the parameter through.

    ## variadic arguments
    If the decorator finds a variadic parameter with an annotation,
    it converts all values bound to that parameter using the annotation

    ## converters
    A converter in this context is a callable that takes one positional argument and returns a value;
    for example, `int` takes a string and returns an integer, or `str.split`
    takes a string and returns a list of strings.

    If a converter can't run with exactly one argument, it raises a `TypeError` on call.

    If a return annotation is given and callable, and the return value of the wrapped function is a tuple,
    the annotation will be called with the elements of the return value.

    ## Example:
    ```py
    @convert
    def f(x: int):
        print(type(x))  # always int, if the value can be converted

    @convert
    def g(x: int) -> isinstance:  # x will be converted to int
        return x, int  # this calls `isinstance(x, int)` (always returns True)
    ```
    """
    sig = signature(f)

    @wraps(f, [i for i in WRAPPER_ASSIGNMENTS if i != "__annotations__"])
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        converted_args = tuple(
            _convert_param(k, bound, v)
            for k, v in sig.parameters.items()
            if v.kind == Parameter.POSITIONAL_ONLY
        )
        var_keyword = {}
        for name, p in sig.parameters.items():
            if p.kind == Parameter.VAR_KEYWORD:
                var_keyword = _convert_param(name, bound, p)
                break
        converted_kwargs = {
            k: _convert_param(k, bound, v)
            for k, v in sig.parameters.items()
            if v.kind in {Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY}
        } | var_keyword
        result = f(*converted_args, **converted_kwargs)

        if (
            isinstance(sig.return_annotation, Callable)
            and sig.return_annotation != Signature.empty
        ):
            if isinstance(result, tuple):
                return sig.return_annotation(*result)
            return sig.return_annotation(result)
        return result

    return wrapper
