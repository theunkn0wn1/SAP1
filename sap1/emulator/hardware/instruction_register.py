import dataclasses

from bitarray import bitarray

from .component_bases import BusComponent
from .register import Register


@dataclasses.dataclass
class InstructionRegister(Register):
    """
    Instruction register subclass
    """
    name: str = 'I'  # IR is always the I register

    @property
    def opcode(self) -> bitarray:
        """
        Stored opcode

        Returns:
            size 4 bitarray opcode
        """
        return self.memory[:4]

    @property
    def operand(self):
        """
        The four least significant bits, representing the instruction's operand

        Returns:
            size 4 bitarray operand
        """
        return self.memory[4:]

    def write(self) -> None:
        # the IR only outputs operand, puling the 4 MSB bits low
        word = bitarray('0000') + self.operand
        BusComponent.bus_state = word
