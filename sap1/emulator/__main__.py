import argparse
import logging
import pathlib

from bitarray import bitarray
from humanfriendly import AutomaticSpinner
from humanfriendly.cli import warning

from . import hardware

LOG = logging.getLogger(f"sap1.{__name__}")

__version__ = "0.1.0"
__author__ = "Joshua (Theunkn0wn1) Salzedo"


def load_memory_from_buffer(buffer: str):
    lines = buffer.split("\n")

    assert len(lines) == 16, f"memory is of an invalid size( {len(lines)}, should be exactly 16 )  "

    for i, line in enumerate(lines):
        mar.memory = bitarray(f"{i:0>4b}")
        ram.value = bitarray(line)


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
        warning(f"unable to locate memory profile {memory_target}. Stop.")
        exit(1)

    if not memory_target.is_file():
        warning(f"{memory_target} is not a file. Stop.")
        exit(1)

    with AutomaticSpinner("pre flight checks passed. initializing...."):
        print("initializing components...")
        register_a = hardware.Register('A')
        register_b = hardware.Register('B')
        instruction_register = hardware.InstructionRegister()
        mar = hardware.Mar()
        control = hardware.ControlUnit(instruction_register)
        ram = hardware.Ram(mar)
        print("OK.\nLoading memory profile from disk....")
        raw_memory = memory_target.read_text()
        print("OK.")
        print("Applying memory profile....")
        load_memory_from_buffer(raw_memory)
        print("OK.")
    print(f"{' Ready. ':-^120}")
