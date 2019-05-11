import functools
import logging
import typing

from sap1.types import MISSING, nibble

LOG = logging.getLogger(f"sap1.{__name__}")


def validate_ptr(func: typing.Callable) -> typing.Callable:
    """
    Wrapping decorator that validates the `ptr` argument

    Args:
        func (typing.Callable): function to protect

    Returns:
        (typing.Callable) decorator instance
    """

    @functools.wraps(func)
    def guarded(*args, ptr, **kwargs):
        assert ptr is not MISSING, "ptr agument cannot be MISSING"
        if isinstance(ptr, int):
            # left pad binary representation of ptr with zeros, then build a bitarray from that
            ptr = nibble(ptr)

        # assertion passed, call the underlying
        return func(*args, ptr=ptr, **kwargs)

    return guarded
