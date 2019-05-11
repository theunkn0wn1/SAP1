import pytest
from bitarray import bitarray

from sap1.instruction_set.microcode import Microcode
from sap1.types import Bit, LOW


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (1, 0, 1),
        (20, 20, 40),
        (250, 10, 4),
        (20, 250, 14)
    ])
def test_add(a_register_fx, b_register_fx, alu_fx, a, b, expected):
    """
    Tests ALU addition
    """

    a_register_fx.memory = bitarray(bin(a)[2:])
    b_register_fx.memory = bitarray(bin(b)[2:])

    with a_register_fx.signal(Microcode(SUB=Bit(LOW))):
        result = alu_fx.value

    result_as_int = int(result.to01(), 2)

    assert expected == result_as_int, "ALU did not return correct value"
