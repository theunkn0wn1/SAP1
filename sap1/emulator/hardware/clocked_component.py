from __future__ import annotations

import abc
import logging
import typing
from dataclasses import dataclass

from sap1.instruction_set.microcode import Microcode

LOG = logging.getLogger(f"sap1.{__name__}")


@dataclass
class ClockedComponent(abc.ABC):
    __components: typing.ClassVar[typing.List[ClockedComponent]] = []

    def __post_init__(self):
        print("ClockedComponent.__init__ called")
        # append the clocked component to builtin registry
        self.__components.append(self)
        super(ClockedComponent, self).__init__()

    @abc.abstractmethod
    def on_clock_high(self, microcode: Microcode):
        """
        Fired on the clock's rising edge

        Args:
            microcode (Microcode): control word
        """

    @abc.abstractmethod
    def on_clock_low(self, microcode: Microcode):
        """
        Fired on the clock's falling edge

        Args:
            microcode (Microcode):

        Returns:

        """

    @classmethod
    def _clock_tick(cls, microcode: Microcode):
        """
        Emit clock events to all Clocked Components

        Args:
            microcode(Microcode): control word to emit

        """

        # emit rising edge
        for component in cls.__components:
            component.on_clock_high(microcode=microcode)

        # emit falling edge
        for component in cls.__components:
            component.on_clock_low(microcode=microcode)
