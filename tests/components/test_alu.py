import pytest
from bitarray import bitarray

from sap1.instruction_set.microcode import Microcode
from sap1.types import Bit, LOW, HIGH


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

    assert result_as_int == expected, "ALU did not return correct value"


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (1, 0, 1),
        (20, 20, 0),
        (250, 10, 240),
        (20, 250, 26)
    ])
def test_subtract(a_register_fx, b_register_fx, alu_fx, a, b, expected):
    """
    Tests ALU subtraction
    """
    a_register_fx.memory = bitarray(f"{a:0>8b}")
    b_register_fx.memory = bitarray(f"{b:0>8b}")

    with a_register_fx.signal(Microcode(SUB=Bit(HIGH))):
        result = alu_fx.value
        result_b = int(alu_fx)

    result_as_int = int(result.to01(), 2)

    assert result_as_int == expected, "ALU did not return correct value"
    assert result_b == expected and result_b == result_as_int, "int(ALU) returns an inconsistent value!"
