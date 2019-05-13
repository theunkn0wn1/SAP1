from __future__ import annotations

import pathlib
from argparse import Namespace
from dataclasses import dataclass

from bitarray import bitarray
from humanfriendly import AutomaticSpinner

from sap1.emulator import hardware
from sap1.emulator.hardware import Mar, Ram
from sap1.emulator.hardware.register import RegisterReadOnly


@dataclass
class Computer:
    program_counter: hardware.ProgramCounter = hardware.ProgramCounter()
    instruction_register: hardware.InstructionRegister = hardware.InstructionRegister()
    mar: hardware.Mar = hardware.Mar()
    control: hardware.ControlUnit = hardware.ControlUnit(instruction_register)
    ram: hardware.Ram = hardware.Ram(mar)
    output_register: RegisterReadOnly = RegisterReadOnly('O')
    register_a: hardware.Register = hardware.Register('A')
    register_b: hardware.Register = hardware.Register('B')
    alu: hardware.ALU = hardware.ALU(register_a, register_b)


def load_memory_from_buffer(buffer: str, mar: Mar, ram: Ram):
    lines = buffer.rstrip().split("\n")

    assert len(lines) == 16, f"memory is of an invalid size( {len(lines)}, should be exactly 16 )  "

    for i, line in enumerate(lines):
        mar.memory = bitarray(f"{i:0>4b}")
        ram.value = bitarray(line)
        assert len(ram.value) == 8, "invalid memory word!"
        print(ram.value)


def runtime(memory_path: pathlib.Path, configuration: Namespace, computer: Computer):
    with AutomaticSpinner("pre flight checks passed. initializing...."):
        print("initializing components...")

        computer = init_components()

        print(f"OK.\nLoading memory profile {memory_path.resolve()} ....")
        raw_memory = memory_path.read_text()
        print("OK.")

        print("Applying memory profile....")
        load_memory_from_buffer(raw_memory, computer.mar, computer.ram)

        print("OK.")
    print(f"{' Ready. ':-^120}")
    if configuration.non_interactive:
        print("running in non-interactive mode...")

        with AutomaticSpinner("executing program..."):
            # run til we reach a HALT or a OUT instruction
            should_stop = False
            while not should_stop:
                should_stop = computer.control.word.HLT or (
                        computer.control.word.OI and configuration.pause_on_out)
                computer.control._clock_tick()

            # step one forward so the output operation can run its course
            computer.control._clock_tick()
            print(f"result:= {computer.output_register.memory}")
            print(f"control word:= {computer.control.word}")
    else:
        print("running in interactive mode... press <enter> to step forward")
        should_stop = False
        while not should_stop:
            computer.control._clock_tick()
            print(f"{'stepping...':-^120}")
            print(
                f"timestep: {computer.control.time_step} \t program_counter {computer.program_counter}\n")
            print(
                f"opcode: {computer.instruction_register.opcode}\toperand{computer.instruction_register.operand}\n")
            print(
                f"control word: {computer.control.word} \n instruction_register {computer.instruction_register}\n")
            print(f"mar: {computer.mar}\tram value:{computer.ram.value}\n")
            print(
                f"a_register: {computer.register_a.memory}\t b_register: {computer.register_b.memory}\n")
            print(f"output register: {computer.output_register.memory}\n")
            input("press enter to step forward")

            should_stop = computer.control.word.HLT or computer.control.word.OI


def init_components():
    return Computer()
