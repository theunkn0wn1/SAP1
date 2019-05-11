from __future__ import annotations

import dataclasses
import logging
import typing

from bitarray import bitarray

LOG = logging.getLogger(f"mecha.{__name__}")


@dataclasses.dataclass
class BusComponent:
    bus_state: typing.ClassVar[bitarray]
