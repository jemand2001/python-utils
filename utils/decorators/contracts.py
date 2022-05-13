from functools import wraps
from inspect import signature
from typing import Callable, Any, Tuple
from functools import partial


def precondition(description: str, c_args: Tuple[str, ...], condition: Callable[..., bool], /) -> Callable:
    """
    decorator to check one precondition of a function (chain to check multiple preconditions)

    :param description: description of the precondition
    :param c_args: arguments of the function
    :param condition: condition to check
    :return: the decorator that checks the precondition

    :Example:
    ```py
    @precondition("x > 0", ("x",), lambda x: x > 0)
    def f(x):
        return x + 1
    
    f(1)  # returns 2
    f(-1)  # raises ValueError

    @precondition("x > 0", ("x",), lambda x: x > 0)
    @precondition("y > 0", ("y",), lambda y: y > 0)
    def f(x, y):
        return x + y
    
    f(1, 1)  # returns 2
    f(1, -1)  # raises ValueError
    f(-1, 1)  # raises ValueError
    f(-1, -1)  # raises ValueError
    ```
    """
    def decorator(func):
        sig = signature(func)
        @wraps(func)
        def wrapper(*args, **kwargs):
            call = sig.bind(*args, **kwargs)
            c_values = [call.arguments.get(arg, None) for arg in c_args]
            if not condition(*c_values):
                raise ValueError(f"{description} condition not satisfied")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def postcondition(description: str, condition: Callable[..., bool], /) -> Callable:
    """
    decorator to check return value of a function for one postcondition (chain for multiple)

    :param description: description of the postcondition
    :param condition: condition to check
    :return: the decorator that checks the postcondition

    :Example:
    ```py
    @postcondition("return > 0", lambda x: x > 0)
    def f(x):
        return x + 1

    f(1)  # returns 2
    f(-1)  # raises ValueError

    @postcondition("return > 0", lambda y: y > 0)
    def f(x, y):
        return x + y
    
    f(1, 1)  # returns 2
    f(1, -1)  # raises ValueError
    f(-1, 1)  # raises ValueError
    f(-1, -1)  # raises ValueError
    ```
    """
    c_sig = signature(condition)
    def decorator(func):
        f_sig = signature(func)
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal condition
            call = f_sig.bind(*args, **kwargs)
            if 'self' in c_sig.parameters:
                condition = partial(condition, self=call.arguments['self'])
            res = func(*args, **kwargs)
            if not condition(res):
                raise ValueError(f"{description} condition not satisfied")
            return res
        return wrapper
    return decorator
