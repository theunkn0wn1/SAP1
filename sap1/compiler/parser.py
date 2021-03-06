"""
ASM parsing library
"""
from __future__ import annotations

import logging
import pathlib
import typing

from .. import instruction_set
from ..instruction_set import Instruction
from sap1.types import MISSING, nibble

LOG = logging.getLogger(f"sap1.{__name__}")


def get_instruction_func(mnemonic: str) -> typing.Callable:
    """
    Yields the instruction constructor for the given mnemonic

    Args:
        mnemonic (str): mnemonic  to find the constructor for

    Returns:
        (typing.Callable) constructor

    Raises:
        AttributeError: constructor not found
    """
    return getattr(instruction_set, mnemonic.lower())


def parse_line(line: str) -> typing.Optional[Instruction]:
    """
    processes a ASM line into an instruction
    Args:
        line (str):  line to process

    Returns:
        (typing.Optional[Instruction]) evaluated instruction, if one was
        evaluated

    Notes:
        lines starting with `#` will be ignored (and return None)
        if a `#` exists within a line, it will be ignored.
        `#` is a comment.
    """

    # split the line up based on the presence of a comment
    sanitized_line = line.split("#")
    LOG.debug(f"sanitized_line = {sanitized_line}")
    words = sanitized_line[0]
    # comment might not exist
    comment = sanitized_line[1] if len(sanitized_line) == 2 else None
    LOG.debug(f"words(pre-strip):= {words}\tcomment:={comment}")
    # strip leading and trailing whitespace, ASM does not use whitespace for
    # control structures (or at least ours doesn't)
    words = words.strip()
    # split the words up into symbols
    symbols = words.split()
    LOG.debug(f"symbols := {symbols}")
    if len(symbols) == 1:
        symbols.append(MISSING)

    # sanity check
    assert len(symbols) == 2, f"invalid ASM instruction '{line}'"
    # unpack mnemonic and operand from symbols
    mnemonic, operand = symbols
    # get the constructor and build the instruction

    constructor = get_instruction_func(mnemonic)
    LOG.debug(f"constructor := {constructor}")
    LOG.debug(f"operand:= {operand}")
    # cast the ptr to a nibble if the operand is not MISSING
    # ptr is expected to be a base 16 value
    ptr = nibble(int(operand, 16 if len(operand) == 1 else 10)) if operand is not MISSING else MISSING
    LOG.debug(f"operand:= {operand}\tptr:={ptr}")
    return constructor(ptr=ptr)


def parse_file(path: pathlib.Path) -> typing.List[Instruction]:
    """
    Parse the specified ASM file into a list of Instruction objects

    Args:
        path (pathlib.Path): path to target ASM

    Returns:
        List of :class:`Instruction` objects
    """
    # read the file into memory
    data = path.read_text()
    # split each line off
    lines = data.split("\n")
    # filter out empty lines and lines that just contain whitespace
    # as well as those that start with comments
    lines = [line for line in lines if
             not (line.isspace() or not line or line.rstrip().startswith("#"))]
    instructions = []
    for i, line in enumerate(lines):
        # parse each line
        try:
            instruction = parse_line(line)
        except Exception as exc:
            logging.exception(f"failed to process ASM line {i}.")
            raise
        # and if it contained an instruction, add it to our collection
        if instruction:
            instructions.append(instruction)

    # returned parsed lines
    return instructions
