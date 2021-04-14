from inspect import signature, Signature
from collections import defaultdict
from functools import wraps
from typing import Callable, MutableMapping
from .strict import is_empty


__all__ = ['overload']


overloaded: MutableMapping[str, MutableMapping[Signature, Callable]] = defaultdict(dict)

def to_string(args, kwargs) -> str:
    return '(' + ', '.join((', '.join(map(repr, args)), ', '.join(f'{k}={v}' for k, v in kwargs.items()))) + ')'

def overload(f: Callable):
    name = f.__qualname__
    overloaded[name][signature(f)] = f

    @wraps(f)
    def wrapper(*args, **kwargs):
        to_call = None
        for sig, func in overloaded[name].items():
            try:
                arguments = sig.bind(*args, **kwargs)
                if to_call is not None:
                    raise ValueError(f'Ambiguous overload for {name}!')
                if all(
                        is_empty(sig.parameters[k].annotation)
                        or isinstance(v, sig.parameters[k].annotation)
                        for k, v in arguments.arguments.items()
                ):
                    to_call = func
            except TypeError:
                continue
        if to_call is None:
            raise ValueError(f'No overloads for {name} with arguments: {to_string(args, kwargs)}')
    return wrapper
