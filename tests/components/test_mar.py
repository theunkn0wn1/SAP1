from bitarray import bitarray

from sap1.instruction_set.microcode import Microcode
from sap1.types import Bit, HIGH


def test_read(mar_fx):
    # populate the bus
    with mar_fx.set_bus_state(bitarray('11011111')):
        # load the MAR from nowhere in specific
        with mar_fx.signal(Microcode(MI=Bit(HIGH))):
            # tick tock.
            mar_fx._clock_tick()

    assert mar_fx.memory == bitarray('1111')
