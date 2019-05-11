import dataclasses
import typing

from sap1.instruction_set.microcode import Microcode


@dataclasses.dataclass
class Component:
    control_word: typing.ClassVar[Microcode] = Microcode()
