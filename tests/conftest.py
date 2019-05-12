import pytest

from sap1.emulator.hardware.alu import ALU
from sap1.emulator.hardware.component_bases import BusComponent
from sap1.emulator.hardware.instruction_register import InstructionRegister
from sap1.emulator.hardware.mar import Mar
from sap1.emulator.hardware.memory import Ram
from sap1.emulator.hardware.program_counter import ProgramCounter
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


@pytest.fixture
def program_counter_fx():
    return ProgramCounter()


@pytest.fixture
def mar_fx() -> Mar:
    return Mar()


@pytest.fixture
def ram_fx(mar_fx) -> Ram:
    return Ram(mar_fx)


@pytest.fixture(autouse=True)
def reset_globals_fx():
    yield
    BusComponent.bus_state.setall(0)
