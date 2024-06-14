"""!
Adds a cache decorator
"""
from enum import Enum
from functools import wraps

__all__ = ["cached", "CacheMissException", "Policy"]


class CacheMissException(Exception):
    """!
    Exception thrown when there is a cache miss when `__cache_policy__` is Policy.only_cache
    """
    pass


class Policy(Enum):
    """!
    Enum describing how the cache should be tried.
    """

    ## try the cache, fetch a new value if it doesn't exist
    try_cache = "try cache"

    ## do not try the cache
    no_cache = "no cache"

    ## only try the cache, throwing CacheMissException if it doesn't exist
    only_cache = "only cache"


def cached(f):
    """!
    A decorator that adds a cache to a function

    The returned function can be configured at the callsite
    by passing a `__cache_control__` keyword parameter that will not be passed to the decorated function.

    @param f the decorated function
    """
    cache = {}

    @wraps(f)
    def wrapper(*args, __cache_policy__=Policy.try_cache, **kwargs):
        """!
        @param __cache_control__ a Policy enum member
        """
        policy = __cache_policy__
        all_args = (args, tuple(kwargs.items()))
        if all_args in cache and policy is not Policy.no_cache:
            return cache[all_args]
        elif policy is Policy.only_cache:
            raise CacheMissException("argument list was not cached")
        res = f(*args, **kwargs)
        cache[all_args] = res
        return res

    return wrapper
