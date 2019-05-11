import pytest
from bitarray import bitarray

from sap1.emulator.hardware.component_bases import BusComponent


@pytest.mark.parametrize("value, expected_opcode, expected_operand",
                         (
                                 (bitarray('01000000'), bitarray('0100'), bitarray('0000')),
                                 (bitarray('11111111'), bitarray('1111'), bitarray('1111')),
                                 (bitarray('10000100'), bitarray('1000'), bitarray('0100')),
                         ))
def test_opcode_and_operand(instruction_register_fx, value: bitarray, expected_opcode,
                            expected_operand):
    """
    validates the opcode and operand properties work as intended
    """
    instruction_register_fx.memory = value
    assert instruction_register_fx.opcode == expected_opcode, "opcode mismatch"
    assert instruction_register_fx.operand == expected_operand, "operand mismatch"


@pytest.mark.parametrize("value, expected_value",
                         (
                                 (bitarray('11110001'), bitarray('00000001')),
                                 (bitarray('00001111'), bitarray('00001111')),
                                 (bitarray('00101100'), bitarray('00001100')),
                                 (bitarray('11100000'), bitarray('00000000'))
                         ))
def test_write(instruction_register_fx, value: bitarray, expected_value):
    instruction_register_fx.memory = value
    instruction_register_fx.write()
    assert BusComponent.bus_state == expected_value, "write failed!"