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
    memory: bitarray = bitarray(8)

    def __post_init__(self):
        # emit event to superclass
        super().__post_init__()
        self.reset()
        try:
            getattr(Microcode(), f"{self.name}I")
        except AttributeError:
            LOG.exception(f"unable to locate relevant control signal, invalid name!")

    def on_clock_high(self):
        LOG.debug(f"register got a high clock event with {self.control_word}")
        # get our read flag from the control signal
        read_flag = getattr(self.control_word, f"{self.name}I")
        write_flag = getattr(self.control_word, f"{self.name}O")

        # check if we are read enabled
        if read_flag:
            self.read()
        # check if we are write enabled
        if write_flag:
            self.write()

        # TODO: what happens when both flags are set? race condition?

    def on_clock_low(self):
        LOG.debug(f"register got a low clock event with {self.control_word}")

    def read(self) -> bitarray:
        """
        read from the bus, set our internal state to match

        Returns:
            (bitarray) new state
        """
        # copy is needed here to decouple memory's internal state from the bus
        self.memory = BusComponent.bus_state.copy()
        return self.memory

    def write(self) -> None:
        """
        Write internal memory to bus
        """
        # copy() is needed here to decouple the bus from the memory's internal state
        BusComponent.bus_state = self.memory.copy()

    def reset(self) -> None:
        """
        Reset internal memory state to zero
        """
        self.memory.setall(0)

    def __int__(self):
        return int(self.memory.to01(), 2)

    def __index__(self):
        return int(self)
