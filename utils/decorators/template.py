"""!
Adds a way to template classes
"""
from typing import Type, TypeVar, Callable
from functools import lru_cache

__all__ = ["template"]

## @cond
T = TypeVar("T")
## @endcond


def template(*args: str):
    """!
    A class template decorator.

    This decorator is supposed to act similarly to C++'s `template` keyword for classes.

    Example:

    ```py
    @template('test')
    class Example:
        def f(self):
            return self.test

    example = Example(test=12)()
    print(example.f())  # prints 12
    ```
    @param args the template parameter names
    """

    def decorator(cls: Type) -> Callable[..., type]:
        @lru_cache(None)
        def wrapper(**kwargs):
            masked = {k: v for k, v in kwargs.items() if k in args}
            name = (
                f"{cls.__qualname__}("
                + ", ".join(f"{k}={v}" for k, v in masked.items())
                + ")"
            )
            meta = type(cls)
            actual = meta(name, tuple(cls.mro())[1:], cls.__dict__ | masked)
            return actual

        return wrapper

    return decorator
