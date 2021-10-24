from dis import Bytecode
from inspect import signature


__all__ = ['auto_slots']


def auto_slots(cls: type) -> type:
    """The auto_slots decorator.
    
    This class decorator will automatically generate a `__slots__` attribute ("make your class slotted")
    based on the attribute assignments to `self` in the decorated class' `__init__` method.
    
    If your class already uses slots, this decorator has no effect. It is intended if you want to benefit
    from making your classes slotted, but don't want to go through and figure out which slots you need;
    You can just put `@auto_slots` in front of your class, and now your class is slotted
    
    ## Example:

    ### This is the intended use
    ```py
    @auto_slots
    class C:
        def __init__(self, x, y):
            self.x = x
            self.y = y + 1
            self.z = []
    print(C.__slots__)  # prints ('x', 'y', 'z')
    ```

    ### While not incorrect, this may be unexpected
    ```py
    @auto_slots
    class C:
        __slots__ = ['x']
        # no explicit __init__ => would take object.__init__ (which doesn't define any attributes)
        def set_x(self, val):
            self.x = val  # no error: C already has a __slots__ attribute
    ```
    """
    if hasattr(cls, '__slots__'):
        return cls
    slots = set()
    bytecode = Bytecode(cls.__init__)
    self_name = next(signature(cls.__init__).parameters.keys())
    instructions = tuple(bytecode)
    for idx, instruction in enumerate(instructions[2:], 2):
        if instruction.opcode == 95 and (instr1 := instructions[idx-1]).opcode == 124 and instr1.argval == self_name:
            slots.add(instruction.argval)

    meta = type(cls)
    return meta(cls.__name__, tuple(cls.mro()), dict(cls.__dict__) | {'__slots__': tuple(slots)})
