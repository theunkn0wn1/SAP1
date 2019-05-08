from typing import Union

from bitarray import bitarray

from ._instruction import Instruction
from .microcode import Microcode, NO_OP
from .types import Bit, nibble

FETCH_STATE = [
    Microcode(MI=Bit(1), OC=Bit(1)),
    Microcode(CE=Bit(1)),
    Microcode(RO=Bit(1), II=Bit(1)),
]


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
        *FETCH_STATE,  # unpack the fetch state
        Microcode(MI=Bit(1), IO=Bit(1)),  # load operand into MAR from IR
        Microcode(RO=Bit(1), AI=Bit(1)),  # load *operand from RAM into Register A
        NO_OP  # t=6, no operation
    ]
    if isinstance(ptr, int):
        # left pad binary representation of ptr with zeros, then build a bitarray from that
        ptr = nibble(ptr)
    return Instruction(phonemic="LDA", opcode=opcode, states=states, operand=ptr)


def hlt() -> Instruction:
    """
    Halt instruction

    Returns:
        (Instruction) halt object
    """

    opcode = bitarray('0000')
    states = [
        *FETCH_STATE,  # unpack the fetch state
        Microcode(HLT=Bit(1)),  # t=3, set halt high
        NO_OP,  # t=5, no operation
        NO_OP  # t=6, no operation
    ]

    return Instruction(phonemic="HLT", opcode=opcode, states=states)
