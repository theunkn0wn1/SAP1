import pathlib
from argparse import Namespace

from bitarray import bitarray
from humanfriendly import AutomaticSpinner

from sap1.emulator import hardware
from sap1.emulator.hardware import Mar, Ram
from sap1.emulator.hardware.register import RegisterReadOnly


def load_memory_from_buffer(buffer: str, mar: Mar, ram: Ram):
    lines = buffer.rstrip().split("\n")

    assert len(lines) == 16, f"memory is of an invalid size( {len(lines)}, should be exactly 16 )  "

    for i, line in enumerate(lines):
        mar.memory = bitarray(f"{i:0>4b}")
        ram.value = bitarray(line)
        assert len(ram.value) == 8, "invalid memory word!"
        print(ram.value)


def runtime(memory_path: pathlib.Path, configuration: Namespace):
    with AutomaticSpinner("pre flight checks passed. initializing...."):
        print("initializing components...")

        (control, instruction_register, mar, output_register, program_counter, ram,
         register_a, register_b, alu) = init_components()

        print(f"OK.\nLoading memory profile {memory_path.resolve()} ....")
        raw_memory = memory_path.read_text()
        print("OK.")

        print("Applying memory profile....")
        load_memory_from_buffer(raw_memory, mar, ram)

        print("OK.")
    print(f"{' Ready. ':-^120}")
    if configuration.non_interactive:
        print("running in non-interactive mode...")

        with AutomaticSpinner("executing program..."):
            # run til we reach a HALT or a OUT instruction
            should_stop = False
            while not should_stop:
                should_stop = control.word.HLT or (control.word.OI and configuration.pause_on_out)
                control._clock_tick()

            # step one forward so the output operation can run its course
            control._clock_tick()
            print(f"result:= {output_register.memory}")
            print(f"control word:= {control.word}")
    else:
        print("running in interactive mode... press <enter> to step forward")
        should_stop = False
        while not should_stop:
            control._clock_tick()
            print(f"{'stepping...':-^120}")
            print(f"timestep: {control.time_step} \t program_counter {program_counter}\n")
            print(f"opcode: {instruction_register.opcode}\toperand{instruction_register.operand}\n")
            print(f"control word: {control.word} \n instruction_register {instruction_register}\n")
            print(f"mar: {mar}\tram value:{ram.value}\n")
            print(f"a_register: {register_a.memory}\t b_register: {register_b.memory}\n")
            print(f"output register: {output_register.memory}\n")
            input("press enter to step forward")

            should_stop = control.word.HLT or control.word.OI


def init_components():
    program_counter = hardware.ProgramCounter()
    instruction_register = hardware.InstructionRegister()
    mar = hardware.Mar()
    control = hardware.ControlUnit(instruction_register)
    ram = hardware.Ram(mar)
    output_register = RegisterReadOnly(name='O')
    register_a = hardware.Register('A')
    register_b = hardware.Register('B')
    alu = hardware.ALU(register_a, register_b)
    return (control, instruction_register, mar, output_register, program_counter, ram, register_a,
            register_b, alu)
