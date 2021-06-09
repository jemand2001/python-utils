from typing import Union, get_origin, get_args, Tuple, Any

__all__ = ['is_instance']

def is_instance(obj: Any, types: Union[type, Tuple[type]]) -> bool:
    """
    ### a wrapper around isinstance that has support for subscripted Unions
    
    obj: the object to test

    types: a type or a tuple of types
    """    
    if get_origin(types) is Union:
        return is_instance(obj, get_args(types))
    
    return isinstance(obj, types)
