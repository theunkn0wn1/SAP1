import argparse
import logging
import pathlib

from humanfriendly.cli import warning

from sap1.emulator._runtime import runtime

LOG = logging.getLogger(f"sap1.{__name__}")

__version__ = "0.1.0"
__author__ = "Joshua (Theunkn0wn1) Salzedo"

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
    print(f"my working directory is {pathlib.Path().resolve()}")
    parser = argparse.ArgumentParser("python -m sap1.emulator")
    parser.add_argument("memory", help="location of memory file")
    parser.add_argument("--non-interactive", help="run until a HLT or OUT instruction is reached",
                        action="store_true")
    parser.add_argument("--pause-on-out", "-pauseOut", help="pause after OUT directives",
                        action="store_true")

    namespace = parser.parse_args()

    memory_target = pathlib.Path(namespace.memory)
    if not memory_target.exists():
        warning(f"unable to locate memory profile {memory_target} Stop.")
        exit(1)

    if not memory_target.is_file():
        warning(f"{memory_target.resolve()} is not a file. Stop.")
        exit(1)

    runtime(memory_target, namespace)
