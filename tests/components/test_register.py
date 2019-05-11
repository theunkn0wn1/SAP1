import pytest
from bitarray import bitarray

from sap1.emulator.hardware.component_bases import BusComponent
from sap1.instruction_set.microcode import Microcode
from sap1.types import HIGH


@pytest.mark.parametrize("value", [1, 2, 255, 12])
def test_read(a_register_fx, value):
    BusComponent.bus_state = bitarray(f"{value:0>b}")
    with a_register_fx.signal(Microcode(AI=HIGH)):
        a_register_fx._clock_tick()

    assert int(a_register_fx) == value, "register did not contain expected value!"
