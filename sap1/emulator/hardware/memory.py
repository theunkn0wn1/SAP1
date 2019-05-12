import typing
from dataclasses import dataclass

from bitarray import bitarray

from .component_bases import ClockedComponent, BusComponent
from .mar import Mar


@dataclass
class Ram(ClockedComponent, BusComponent):
    mar: Mar
    memory: typing.Dict[str, bitarray] = None

    def __post_init__(self):
        # if we have not already initialized our memory
        if not self.memory:
            # use a dict comprehension to initialize all 16 memory addresses
            self.memory = {f'{count:0>4b}': bitarray('00000000') for count in range(16)}
        # ensure the super gets called
        super(Ram, self).__post_init__()

    def on_clock_high(self):
        if self.control_word.RI:
            # mar in, copy the bus state into storage
            self.value = self.bus_state.copy()

    def on_clock_low(self):
        if self.control_word.RO:
            BusComponent.bus_state = self.value.copy()

    @property
    def value(self):
        # return value stored at the MAR
        return self.memory[self.mar.memory.to01()]

    @value.setter
    def value(self, new_value: bitarray):
        self.memory[self.mar.memory.to01()] = new_value

    ...
