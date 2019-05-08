import typing

# Bit = typing.NewType("Bit", int)
from typing import Union

from bitarray import bitarray

"""
Binary one or zero
"""

Bit = typing.NewType("Bit", int)


def nibble(ptr: int = 0) -> bitarray:
    """
    return a 0 initialized nibble of bits (4 bits)
    """
    assert 0xf >= ptr >= 0, "value out of range"
    return bitarray(f"{bin(ptr)[2:]:{0}>4}")


Pointer = Union[bitarray, int]
MISSING = object()
"""
Used to represent a missing operand
"""