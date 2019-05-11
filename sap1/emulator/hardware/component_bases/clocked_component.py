from __future__ import annotations

import abc
import logging
import typing
import weakref
from dataclasses import dataclass

from sap1.instruction_set.microcode import Microcode
from .component import Component

LOG = logging.getLogger(f"sap1.{__name__}")


@dataclass
class ClockedComponent(abc.ABC, Component):
    __components: typing.ClassVar[typing.List[ClockedComponent]] = []

    def __post_init__(self):
        """

        Post-initialization routine

        Uses code adapted from https://github.com/fuelrats/pipsqueak3 see attribution.

        Attribution:
            BSD 3-Clause License

            Copyright (c) 2018, The Fuel Rats Mischief
            All rights reserved.
            see 3rd_party/pipsqueak3/LICENSE
        """
        print("ClockedComponent.__init__ called")
        # append the clocked component to builtin registry

        # create a finalizer-based weak reference, tie the callback to our GC method
        # then append it to our storage object
        self.__components.append(weakref.finalize(self, self.__gc))
        super().__init__()

    @abc.abstractmethod
    def on_clock_high(self):
        """
        Fired on the clock's rising edge

        Args:
            microcode (Microcode): control word
        """

    @abc.abstractmethod
    def on_clock_low(self):
        """
        Fired on the clock's falling edge

        Args:
            microcode (Microcode):

        Returns:

        """

    @classmethod
    def _clock_tick(cls):
        """
        Emit clock events to all Clocked Components

        """
        if cls.control_word.HLT:
            # clock is halted, bail out
            LOG.debug("clock is halted, will not emit clock tick.")
            return
        # emit rising edge
        for component in cls.__components:
            component.on_clock_high()

        # emit falling edge
        for component in cls.__components:
            component.on_clock_low()

    @classmethod
    def __gc(cls) -> int:
        """
        Garbage collect dead references. called when a weak reference dies.

        Returns:
            number of references collected


        Attribution:
            BSD 3-Clause License

            Copyright (c) 2018, The Fuel Rats Mischief
            All rights reserved.
            see 3rd_party/pipsqueak3/LICENSE

        """
        # calculate which references are dead
        to_delete = {reference for reference in cls.__components if not reference.alive}

        culled = len(to_delete)
        # and cull them
        for reference in to_delete:
            cls.__components.remove(reference)

        return culled
