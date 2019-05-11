import contextlib
import dataclasses
import functools
import typing

from sap1.instruction_set.microcode import Microcode, NO_OP


@dataclasses.dataclass
class Component:
    control_word: typing.ClassVar[Microcode] = Microcode()

    @classmethod
    @functools.wraps(Microcode)
    @contextlib.contextmanager
    def signal(cls, word: Microcode) -> None:
        """
        temporally  set the control word to `word`, reset to :obj:`NO_OP` on exit

        Args:
            word(Microcode): control word to use on entry

        """
        Component.control_word = word

        yield

        Component.control_word = NO_OP
