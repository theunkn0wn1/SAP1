import dataclasses
import itertools

from bitarray import bitarray

from sap1.emulator.hardware.component_bases import ClockedComponent, BusComponent


@dataclasses.dataclass
class ProgramCounter(ClockedComponent, BusComponent):
    """
    Program counter
    """
    count: int = 0
    _counter = itertools.cycle(range(0b10000))  # range is [a,b), so 0b10000 is excluded

    def jump(self, target: int):
        if target < 0 or target >= 0x10:
            raise ValueError("invalid jump")

        self.count = next(itertools.dropwhile(lambda x: (x != target), self._counter))

    def on_clock_high(self):
        if self.control_word.CE:
            # if clock is enabled then increment internal count
            self.count = next(self._counter)

        if self.control_word.JMP:
            # jump is HIGH, write into our counter
            new_value_arr: bitarray = self.bus_state[4:]
            new_count = int(new_value_arr.to01(), 2)
            self.jump(new_count)

    def on_clock_low(self):
        pass

    def reset(self):
        self.jump(0)
