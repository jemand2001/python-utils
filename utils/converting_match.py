"""!
This module provides a way to bind a match case to a value derived from the one
that is being matched (I know this is a terrible description but bear with me).

## Example:
```py
from utils.converting_match import Converting, pre_made_converters, check_for

JSON = check_for(json.loads)

match Converting(some_string):
    case pre_made_converters.Digits(x):
        assert isinstance(x, int)
    case pre_made_converters.Complex(x):
        assert isinstance(x, complex)
    case JSON(value):
        assert isinstance(value, (dict, list))
```
"""
from contextlib import suppress
from functools import partial
from typing import Any, Final


__all__ = ('Converting', 'check_for', 'pre_made_converters')


class _ConverterMeta(type):
    """!
    The converter metaclass. Do not use directly.
    """
    __converted__ = None
    __original__ = None


def Converting(obj):
    """!
    A wrapper for an object to be used with match cases involving ::check_for.

    For ideal results, type(obj) should implement something akin to a "copy constructor",
    that is, `type(obj)(obj) is obj` should be True (many built-in types do this, so it already works with them).

    @param obj the object to be wrapped
    @return a wrapper object
    """
    class Conv(type(obj), metaclass=_ConverterMeta):
        def __init__(self, obj):
            self.__converted__ = None
            self.__original__: Final = obj
    return Conv(obj)


def check_for(converter):
    """!
    A match case for ::Converting.

    @param converter a callable object that converts the wrapped object to another object
    @return a match case
    """
    class Meta(type):
        __conv__ = staticmethod(converter)
        __match_args__ = ('__converted__',)

        def __instancecheck__(self, instance: Any) -> bool:
            with suppress(ValueError):
                is_converting = isinstance(type(instance), _ConverterMeta)
                if is_converting:
                    assert hasattr(instance, '__converted__')
                    assert hasattr(instance, '__original__')
                value = self.__conv__(instance.__original__ if is_converting else instance)
                if is_converting:
                    instance.__converted__ = value
                return True
            return False
    return Meta(f'check_for({converter!r})', (), {})


class pre_made_converters:
    """!
    Contains some converters
    """
    ## A converter from digits
    Digits = check_for(int)
    ## A converter from hexadecimal
    Hexadecimal = check_for(partial(int, base=16))
    ## A converter from binary
    Binary = check_for(partial(int, base=2))
    ## A converter from octal
    Octal = check_for(partial(int, base=8))
    ## A converter from float
    Float = check_for(float)
    ## A converter from complex
    Complex = check_for(complex)
