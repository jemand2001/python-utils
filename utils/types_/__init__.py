"""!
some additional (math) types you may need, with instance checks
"""


__all__ = ["NaturalNumber", "StrictNaturalNumber"]


class NaturalNumberMeta(type):
    """!
    metaclass
    """

    def __instancecheck__(self, instance):
        """!
        Checks whether the argument is an instance of the type
        @param instance the object to test
        @return the number matches the criteria
        """
        return isinstance(instance, int) and instance >= 0


class StrictNaturalNumberMeta(type):
    """!
    metaclass
    """

    def __instancecheck__(self, instance):
        """!
        Checks whether the argument is an instance of the type
        @param instance the object to test
        @return the number matches the criteria
        """
        return isinstance(instance, int) and instance >= 1


class NaturalNumber(metaclass=NaturalNumberMeta):
    """!
    A natural number is any non-negative integer
    """

    pass


class StrictNaturalNumber(metaclass=StrictNaturalNumberMeta):
    """!
    A strict natural number is any integer bigger than 0
    """

    pass
