import logging
from dataclasses import dataclass

from sap1.instruction_set.microcode import Microcode
from .bus_component import BusComponent
from .clocked_component import ClockedComponent

LOG = logging.getLogger(f"mecha.{__name__}")


@dataclass
class Register(BusComponent, ClockedComponent):
    load_flag: str

    def on_clock_high(self, microcode: Microcode):
        print(f"register got a high clock event with {microcode}")

    def on_clock_low(self, microcode: Microcode):
        print(f"register got a low clock event with {microcode}")
