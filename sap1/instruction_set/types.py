import typing

# Bit = typing.NewType("Bit", int)
from bitarray import bitarray

"""
Binary one or zero
"""

Bit = typing.NewType("Bit", int)


def nibble_factory() -> bitarray:
    """
    return a 0 initialized nibble of bits (4 bits)
    """
    return bitarray('0000')
