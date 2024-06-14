"""!
Adds an "immediately-invoked function" decorator
"""

def evaluated(*args, **kwargs):
    """!
    Evaluate a callable immediately with the given arguments and keyword arguments

    ## Example:
    ```py
    @evaluated(12)
    def f(x):
        return x + 1

    print(f)  # prints 13

    @evaluated(10)
    @dataclass
    class C:
        x: int
    print(C.x)  # prints 10
    ```

    @param args The arguments passed to the function
    @param kwargs The keyword arguments passed to the function
    """

    def decorator(func):
        return func(*args, **kwargs)

    return decorator
