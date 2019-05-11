import dataclasses
import typing

from sap1.instruction_set.microcode import Microcode


@dataclasses.dataclass
class Component:
    control_state: typing.ClassVar[Microcode] = Microcode()
