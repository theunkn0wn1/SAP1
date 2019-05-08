import functools
import logging
import typing

from .types import MISSING

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
        # assertion passed, call the underlying
        return func(*args, ptr=ptr, **kwargs)

    return guarded
