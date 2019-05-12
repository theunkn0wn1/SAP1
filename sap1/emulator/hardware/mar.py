from dataclasses import dataclass

from bitarray import bitarray

from .register import RegisterReadOnly


@dataclass
class Mar(RegisterReadOnly):
    """
    Memory address register
    """
    name: str = 'M'

    def read(self) -> bitarray:
        new_value_arr: bitarray = self.bus_state[4:]
        self.memory = new_value_arr
