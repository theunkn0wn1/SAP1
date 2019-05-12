import dataclasses

from bitarray import bitarray

from sap1.emulator.hardware.component_bases import ClockedComponent, BusComponent


@dataclasses.dataclass
class ProgramCounter(ClockedComponent, BusComponent):
    """
    Program counter
    """
    count: int = 0

    def on_clock_high(self):
        if self.control_word.CE:
            # if clock is enabled then increment internal count
            self.count += 0b1
            if self.count == 0b10000:
                # overflow
                self.count = 0b0

        if self.control_word.JMP:
            # jump is HIGH, write into our counter
            new_value_arr: bitarray = self.bus_state[4:]
            new_count = int(new_value_arr.to01(), 2)
            self.count = new_count

    def on_clock_low(self):
        pass

