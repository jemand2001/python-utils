from inspect import Signature, signature, Parameter, BoundArguments
from typing import Callable, TypeVar, Tuple, Union
from functools import wraps, WRAPPER_ASSIGNMENTS


T = TypeVar('T')


def convert_param(name: str, bound: BoundArguments, param: Parameter) -> Union[T, Tuple[T]]:
    # print(param.annotation)
    if isinstance(param.annotation, Callable) and param.annotation != Parameter.empty:
        func = param.annotation
    else:
        func = lambda x: x
    # print(func)
    if param.kind == Parameter.VAR_POSITIONAL:
        return (*map(func, bound.arguments[name]),)
    elif param.kind == Parameter.VAR_KEYWORD:
        return {k: func(v) for k, v in bound.arguments[name].items()}
    else:
        return func(bound.arguments[name])


def convert(f):
    '''The `convert` decorator.
    
    This decorator allows you to implicitly convert arguments to a function.
    It treats the parameter annotations as converters, if they're callable;
    otherwise it just passes the parameter through.
    
    # variadic arguments
    If the decorator finds a variadic parameter with an annotation,
    it converts all values bound to that parameter using the annotation

    Example:
    ```py
    @convert
    def f(x: int):
        print(type(x))  # always int, if the value can be converted
    ```
    '''
    sig = signature(f)

    @wraps(f, [i for i in WRAPPER_ASSIGNMENTS if i != '__annotations__'])
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        converted_args = tuple(convert_param(k, bound, v) for k, v in sig.parameters.items() if v.kind == Parameter.POSITIONAL_ONLY)
        var_keyword = {}
        for name, p in sig.parameters.items():
            if p.kind == Parameter.VAR_KEYWORD:
                var_keyword = convert_param(name, bound, p)
                break
        converted_kwargs = {
            k: convert_param(k, bound, v)
            for k, v in sig.parameters.items()
            if v.kind in {Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY}
        } | var_keyword
        result = f(*converted_args, **converted_kwargs)
        if isinstance(sig.return_annotation, Callable) and sig.return_annotation != Signature.empty:
            return sig.return_annotation(result)
        return result
    return wrapper

