"""!
Contains a function that extends standard isinstance.
"""
from typing import Union, get_origin, get_args, Tuple, Any

__all__ = ['is_instance']

def is_instance(obj: Any, types: Union[type, Tuple[type]]) -> bool:
    """!
    A wrapper around isinstance that has support for subscripted Unions
    
    @param obj the object to test
    @param types a type or a tuple of types
    """    
    if get_origin(types) is Union:
        return is_instance(obj, get_args(types))
    
    return isinstance(obj, types)
