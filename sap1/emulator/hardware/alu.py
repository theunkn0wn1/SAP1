import dataclasses

from .component_bases import BusComponent
from .register import Register


@dataclasses.dataclass
class ALU(BusComponent):
    """
    ALU emulation class
    """
    A_REGISTER: Register
    B_REGISTER: Register
