from bitarray import bitarray

from sap1.instruction_set import Instruction


def address(instruction: Instruction, time: int) -> int:
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
    return int(word.to01(), 2)
