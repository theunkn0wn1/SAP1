import pytest

from sap1.emulator.hardware.alu import ALU
from sap1.emulator.hardware.instruction_register import InstructionRegister
from sap1.emulator.hardware.register import Register


@pytest.fixture
def a_register_fx() -> Register:
    return Register('a')


@pytest.fixture
def b_register_fx() -> Register:
    return Register('b')


@pytest.fixture
def instruction_register_fx() -> InstructionRegister:
    return InstructionRegister()


@pytest.fixture
def alu_fx(a_register_fx, b_register_fx) -> ALU:
    return ALU(A_REGISTER=a_register_fx, B_REGISTER=b_register_fx)
