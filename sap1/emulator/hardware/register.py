import logging
from dataclasses import dataclass

from bitarray import bitarray

from sap1.instruction_set.microcode import Microcode
from .component_bases import BusComponent
from .component_bases import ClockedComponent

LOG = logging.getLogger(f"sap1.{__name__}")


@dataclass
class Register(ClockedComponent, BusComponent):
    name: str
    memory: bitarray = bitarray('00000000')

    def __post_init__(self):
        # emit event to superclass
        super().__post_init__()
        try:
            getattr(Microcode(), f"{self.name}I")
        except AttributeError:
            LOG.exception(f"unable to locate relevant control signal, invalid name!")

    def on_clock_high(self, microcode: Microcode):
        LOG.debug(f"register got a high clock event with {microcode}")
        # get our read flag from the control signal
        read_flag = getattr(microcode, f"{self.name}I")
        if read_flag:
            self.read()

    def on_clock_low(self, microcode: Microcode):
        LOG.debug(f"register got a low clock event with {microcode}")

    def read(self) -> bitarray:
        """
        read from the bus, set our internal state to match

        Returns:
            (bitarray) new state
        """
        self.memory = self.bus_state
        return self.memory

    def write(self) -> None:
        """
        Write internal memory to bus
        """

        BusComponent.bus_state = self.memory
