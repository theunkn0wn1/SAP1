import typing
from dataclasses import dataclass, field

from bitarray import bitarray

from .microcode import Microcode
from .types import nibble_factory


@dataclass
class Instruction:
    """
    Abstract instruction
    """

    phonemic: str
    opcode: bitarray
    states: typing.List[Microcode]
    operand: bitarray = field(default=nibble_factory)

    def binary(self) -> typing.List[bitarray]:
        """
        Dumps the instruction into its microcode binary

        Returns:
            list of microcode instructions dumped to a bitarray
        """

