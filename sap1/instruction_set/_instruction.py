import typing
from dataclasses import dataclass, field

from bitarray import bitarray

from .microcode import Microcode
from sap1.types import nibble, MISSING


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
        return [state.dump() for state in self.states]

    @property
    def machine_code(self) -> bitarray:
        """
        Returns the machine code representation of the instruction
        """
        # append the operand to the opcode and BAM! machine code
        return self.opcode + (self.operand if self.operand is not MISSING else nibble())
