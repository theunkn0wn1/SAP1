import pytest
from bitarray import bitarray

from sap1.instruction_set.microcode import Microcode, NO_OP
from sap1.types import Bit, HIGH


def test_increment(program_counter_fx):
    """
    Verifies increment nature of the program counter
    """

    program_counter_fx.jump(0)
    # increment clock
    with program_counter_fx.signal(Microcode(CE=Bit(HIGH))):
        program_counter_fx._clock_tick()

    assert program_counter_fx.count == 1, "program counter failed to increment"
    # increment clock
    program_counter_fx.jump(14)
    # increment clock
    with program_counter_fx.signal(Microcode(CE=Bit(HIGH))):
        program_counter_fx._clock_tick()

    assert program_counter_fx.count == 0b1111, "program counter failed to increment"
    # increment clock
    with program_counter_fx.signal(Microcode(CE=Bit(HIGH))):
        program_counter_fx._clock_tick()

    assert program_counter_fx.count == 0b0000, "program counter failed to roll over"


@pytest.mark.parametrize("value, expected", (
        (bitarray('010101100'), 0b1100),
        (bitarray('01011111'), 0b1111),
        (bitarray('01010011'), 0b0011)
))
def test_jump(program_counter_fx, value, expected):
    """
    Test jump control
    """
    # enable JMP flag
    with program_counter_fx.signal(Microcode(JMP=HIGH)):
        with program_counter_fx.set_bus_state(value):
            program_counter_fx._clock_tick()

    assert program_counter_fx.count == expected, "PC jump failure."


def test_no_op(program_counter_fx):
    """
    Test no-op behavior
    """
    program_counter_fx.count = 0

    # put a random value on the bus
    with program_counter_fx.set_bus_state(bitarray('01000010')):
        # and set the signal state to NO_OP
        with program_counter_fx.signal(NO_OP):
            # tick tock.
            program_counter_fx._clock_tick()

    # nothing should happen here, we should still be zero
    assert program_counter_fx.count == 0, "clock changed during a no-op!"


def test_reset(program_counter_fx):
    program_counter_fx.jump(0b1100)

    program_counter_fx.reset()
    assert program_counter_fx.count == 0, "failed to reset PC"
