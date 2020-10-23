from enum import Enum
from functools import wraps

__all__ = ['cached', 'CacheMissException', Policy]


class CacheMissException(Exception):
    pass


def cached_with_policy(f):
    cache = {}

    @wraps(f)
    def wrapper(*args, **kwargs):
        """__cache_control__: a Policy enum member"""
        policy = kwargs.pop("__cache_policy__", Policy.try_cache)
        all_args = (args, tuple(kwargs.items()))
        if all_args in cache and policy is not Policy.no_cache:
            return cache[all_args]
        elif policy is Policy.only_cache:
            raise CacheMissException('argument list was not cached')
        res = f(*args, **kwargs)
        cache[all_args] = res
        return res
    return wrapper


class Policy(Enum):
    try_cache = 'try cache'
    no_cache = 'no cache'
    only_cache = 'only cache'
