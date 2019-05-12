from bitarray import bitarray

from sap1.instruction_set.microcode import Microcode
from sap1.types import Bit, HIGH


def test_read(ram_fx, mar_fx):
    """
    Tests Memory's read behavior\
    """

    expected = bitarray('11011101')
    # manually set an address to expected data
    ram_fx.memory['0010'] = expected

    mar_fx.memory = bitarray('0010')

    assert ram_fx.value == expected


def test_write(ram_fx, mar_fx):
    """ test write behavior """

    expected = bitarray('11011101')
    # manually set an address to expected data
    ram_fx.memory['0010'] = expected

    mar_fx.memory = bitarray('0010')

    with mar_fx.signal(Microcode(RO=Bit(HIGH))):
        mar_fx._clock_tick()
        assert expected == mar_fx.bus_state
