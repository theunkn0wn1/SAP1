from typing import Union

from bitarray import bitarray

from ._instruction import Instruction
from .microcode import Microcode, NO_OP
from .types import Bit


def lda(ptr: Union[bitarray, int]) -> Instruction:
    """
    load the accumulator (A register) with value at *ptr

    Args:
        ptr(bitarray): pointer to memory location to load into memory
        ptr(int): integer representation of pointer
    Returns:
        (Instruction) object
    """
    opcode = bitarray('0000')
    states = [
        Microcode(MI=Bit(1), OC=Bit(1)),
        Microcode(CE=Bit(1)),
        Microcode(RO=Bit(1), II=Bit(1)),
        Microcode(),
        Microcode(),
        NO_OP  # t=6, no operation
    ]
    if isinstance(ptr, int):
        ptr = bitarray(bin(ptr)[2:])
    return Instruction(phonemic="LDA", opcode=opcode, states=states, operand=ptr)
