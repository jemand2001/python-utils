

def evaluated(*args, **kwargs):
    """
    evaluate a callable immediately with the given arguments and keyword arguments
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
    """
    def decorator(func):
        return func(*args, **kwargs)
    return decorator
