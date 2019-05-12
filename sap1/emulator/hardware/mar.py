from dataclasses import dataclass

from bitarray import bitarray

from .register import RegisterReadOnly


@dataclass
class Mar(RegisterReadOnly):
    """
    Memory address register
    """
    name: str = 'M'
    memory: bitarray = bitarray('0000')

    def read(self) -> bitarray:
        new_value_arr: bitarray = self.bus_state[4:]
        self.memory = new_value_arr
