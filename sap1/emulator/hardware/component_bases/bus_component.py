from __future__ import annotations

import contextlib
import dataclasses
import logging
import typing

from bitarray import bitarray

from .component import Component

LOG = logging.getLogger(f"sap1.{__name__}")


@dataclasses.dataclass
class BusComponent(Component):
    bus_state: typing.ClassVar[bitarray] = bitarray('00000000')

    @staticmethod
    @contextlib.contextmanager
    def set_bus_state(state: bitarray) -> None:
        """
        Temporally sets the bus's state to the provided :arg:`state`

        Resets the bus to 0b00000000 on exit

        Args:
            state(bitarray):  value to write onto the bus
        """
        # set bus state to argument
        BusComponent.bus_state = state
        yield
        # reset bus state after
        BusComponent.bus_state.setall(0)
