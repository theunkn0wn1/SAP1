import dataclasses
import itertools
import logging

from bitarray import bitarray

from sap1.firmware import EEPROM_A, EEPROM_B
from sap1.instruction_set.microcode import Microcode
from .component_bases import ClockedComponent
from .instruction_register import InstructionRegister

LOG = logging.getLogger(f"sap1.{__name__}")


@dataclasses.dataclass
class ControlUnit(ClockedComponent):
    """
    The brainz of the machine.
    """
    instruction_register: InstructionRegister
    _counter = itertools.cycle(range(0, 6))  # times [0,6) exclusive
    time_step: int = next(_counter)

    def on_clock_high(self):
        self.time_step = next(self._counter)

    def on_clock_low(self):
        pass

    @property
    def address(self):
        addr: bitarray = self.instruction_register.opcode + bitarray(f"{self.time_step:0>4b}")
        return int(addr.to01(), 2)

    @property
    def word(self) -> Microcode:
        word_a = f"{EEPROM_A[self.address]:0>8b}"
        word_b = f"{EEPROM_B[self.address]:0>8b}"
        int_a = [int(v) for v in word_a]
        int_b =  [int(v) for v in word_b]
        return Microcode(*int_a, *int_b)
# lets build the address
