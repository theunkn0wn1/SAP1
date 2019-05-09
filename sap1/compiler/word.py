from dataclasses import dataclass

from bitarray import bitarray

from sap1.instruction_set import Instruction
from sap1.instruction_set.microcode import Microcode


def address(instruction: Instruction, time: int) -> bitarray:
    """
    Calculate the address of an instruction

    Args:
        instruction:
        time:

    Returns:

    """
    time_bits = bitarray(f"{time:0>3b}")
    word: bitarray = instruction.opcode + time_bits
    # convert to bin, then to int
    return word


@dataclass
class Word:
    address: bitarray
    code: Microcode

    @property
    def word(self):
        return self.code.dump()

    def __index__(self) -> int:
        ...

    def __int__(self) -> int:
        ...
