import typing
from dataclasses import dataclass, field

from bitarray import bitarray

from .microcode import Microcode
from .types import nibble


@dataclass
class Instruction:
    """
    Abstract instruction
    """

    mnemonic: str
    opcode: bitarray
    states: typing.List[Microcode]
    operand: bitarray = field(default=nibble())

    def binary(self) -> typing.List[bitarray]:
        """
        Dumps the instruction into its microcode binary

        Returns:
            list of microcode instructions dumped to a bitarray
        """
        raise NotImplementedError("not implemented yet!")

    @property
    def machine_code(self) -> bitarray:
        """
        Returns the machine code representation of the instruction
        """
        # append the operand to the opcode and BAM! machine code
        return self.opcode + self.operand
