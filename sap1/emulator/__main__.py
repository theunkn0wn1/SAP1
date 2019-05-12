import argparse
import logging
import pathlib

from bitarray import bitarray
from humanfriendly import AutomaticSpinner
from humanfriendly.cli import warning

from sap1.emulator.hardware.register import RegisterReadOnly
from sap1.types import Bit, LOW, HIGH
from . import hardware

LOG = logging.getLogger(f"sap1.{__name__}")

__version__ = "0.1.0"
__author__ = "Joshua (Theunkn0wn1) Salzedo"


def load_memory_from_buffer(buffer: str):
    lines = buffer.rstrip().split("\n")

    assert len(lines) == 16, f"memory is of an invalid size( {len(lines)}, should be exactly 16 )  "

    for i, line in enumerate(lines):
        mar.memory = bitarray(f"{i:0>4b}")
        ram.value = bitarray(line)
        assert len(ram.value) == 8, "invalid memory word!"
        print(ram.value)


if __name__ == '__main__':
    print(f"{'=':=^120}")
    print(r"""
     _____  ___  ______       __    ________  ____   _ _       ___ _____ ___________
    /  ___|/ _ \ | ___ \     /  |  |  ___|  \/  | | | | |     / _ \_   _|  _  | ___ \
    \ `--./ /_\ \| |_/ /_____`| |  | |__ | .  . | | | | |    / /_\ \| | | | | | |_/ /
     `--. \  _  ||  __/______|| |  |  __|| |\/| | | | | |    |  _  || | | | | |    /
    /\__/ / | | || |         _| |_ | |___| |  | | |_| | |____| | | || | \ \_/ / |\ \
    \____/\_| |_/\_|         \___/ \____/\_|  |_/\___/\_____/\_| |_/\_/  \___/\_| \_|
    """)
    print(f"{f' sap-1 emulator v{__version__} by {__author__}':-^120}")
    parser = argparse.ArgumentParser("python -m sap1.emulator")
    parser.add_argument("memory", help="location of memory file")
    parser.add_argument("--non-interactive", help="run until a HLT or OUT instruction is reached",
                        action="store_true")

    namespace = parser.parse_args()

    memory_target = pathlib.Path(namespace.memory)
    if not memory_target.exists():
        warning(f"unable to locate memory profile {memory_target} Stop.")
        exit(1)

    if not memory_target.is_file():
        warning(f"{memory_target.resolve()} is not a file. Stop.")
        exit(1)

    with AutomaticSpinner("pre flight checks passed. initializing...."):
        print("initializing components...")

        program_counter = hardware.ProgramCounter()
        instruction_register = hardware.InstructionRegister()
        mar = hardware.Mar()
        control = hardware.ControlUnit(instruction_register)
        ram = hardware.Ram(mar)
        register_a = hardware.Register('A')
        register_b = hardware.Register('B')
        output_register = RegisterReadOnly(name='O')

        print("OK.\nLoading memory profile from disk....")
        raw_memory = memory_target.read_text()
        print("OK.")

        print("Applying memory profile....")
        load_memory_from_buffer(raw_memory)

        print("OK.")
    print(f"{' Ready. ':-^120}")
    if namespace.non_interactive:
        print("running in non-interactive mode...")

        with AutomaticSpinner("executing program..."):
            # run til we reach a HALT or a OUT instruction
            while (control.word.HLT == Bit(HIGH)) or (control.word.OI == Bit(HIGH)):
                control._clock_tick()

            # step one forward so the output operation can run its course
            control._clock_tick()
            print(f"result:= {output_register.memory}")
            print(f"control word:= {control.word}")
    else:
        print("running in interactive mode... press <enter> to step forward")
        while (control.word.HLT == Bit(LOW)) and (control.word.OI == Bit(LOW)):
            print(f"{'stepping...':-^120}")
            print(f"timestep: {control.time_step} \t program_counter {program_counter}")
            print(f"opcode: {instruction_register.opcode}\toperand{instruction_register.operand}")
            print(f"control word: {control.word} \t instruction_register {instruction_register}")
            print(f"mar: {mar}\tram value:{ram.value}")
            print(f"a_register: {register_a.memory}\t b_register: {register_b.memory}")
            input("press enter to step forward")
            control._clock_tick()
