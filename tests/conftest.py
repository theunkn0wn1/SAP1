import pytest

from sap1.emulator.hardware.alu import ALU
from sap1.emulator.hardware.component_bases import BusComponent
from sap1.emulator.hardware.instruction_register import InstructionRegister
from sap1.emulator.hardware.register import Register


@pytest.fixture
def a_register_fx() -> Register:
    return Register('A')


@pytest.fixture
def b_register_fx() -> Register:
    return Register('B')


@pytest.fixture
def instruction_register_fx() -> InstructionRegister:
    return InstructionRegister()


@pytest.fixture
def alu_fx(a_register_fx, b_register_fx) -> ALU:
    return ALU(A_REGISTER=a_register_fx, B_REGISTER=b_register_fx)


@pytest.fixture(autouse=True)
def reset_globals_fx():
    yield
    BusComponent.bus_state.setall(0)
