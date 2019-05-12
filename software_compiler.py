import argparse
import pathlib

from sap1.compiler.parser import parse_file
from sap1.instruction_set import lda
from sap1.types import MISSING

if __name__ == '__main__':
    # used font = "doom"
    print(r"""
     _____  ___  ______       __    _____ ________  _________ _____ _      ___________
    /  ___|/ _ \ | ___ \     /  |  /  __ \  _  |  \/  || ___ \_   _| |    |  ___| ___ \
    \ `--./ /_\ \| |_/ /_____`| |  | /  \/ | | | .  . || |_/ / | | | |    | |__ | |_/ /
     `--. \  _  ||  __/______|| |  | |   | | | | |\/| ||  __/  | | | |    |  __||    /
    /\__/ / | | || |         _| |_ | \__/\ \_/ / |  | || |    _| |_| |____| |___| |\ \
    \____/\_| |_/\_|         \___/  \____/\___/\_|  |_/\_|    \___/\_____/\____/\_| \_|
    """)
    print(f"{'  SAP-1 compiler by Joshua (Theunkn0wn1) Salzedo  ':-^120}")
    parser = argparse.ArgumentParser(prog="SAP-1 software compiler")
    parser.add_argument("target", type=str)
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--output", help="directory to output machine code into", default=".")

    args = parser.parse_args()

    input_path = pathlib.Path(args.target)
    output_path = pathlib.Path(args.output)
    if not input_path.exists():
        print(f"unable to locate file {input_path}. please check your spelling. Stop.")
        # bail out
        exit(1)
    if not input_path.is_file():
        print(f"directory specified, please give me just the ASM file you want me to compile. Stop.")
        exit(1)

    if not output_path.is_dir():
        print(f"output directory {output_path} is not a directory. Stop.")
        exit(2)

    try:
        instructions = parse_file(input_path)
    except (AssertionError, TypeError, ValueError):
        print("\n\n\n")
        print(f"!!!{'-':->114}!!!")
        print("file parsing failed. check your file.")
        print(f"!!!{'-':->114}!!!")
        exit(2)
    # output block
    print(f"{'parsed asm': >12} | {'addr'} | {'machine code': <30}")

    with (output_path / f"{input_path.stem}.sap1").open('w') as ofile:
        # the only instance its unbound is when the program exits due to an error, hence making
        # this code unreachable. suppress warning.
        # noinspection PyUnboundLocalVariable
        # buffer output to be exactly 16 lines in length
        while len(instructions) < 16:
            instructions.append(lda(ptr=0))
        # the only instance its unbound is when the program exits due to an error, hence making
        # this code unreachable. suppress warning.
        # noinspection PyUnboundLocalVariable
        for i, instruction in enumerate(instructions):
            operand_value = int(instruction.operand.to01(),
                                2) if instruction.operand is not MISSING else 0
            print(
                f"{instruction.mnemonic: >10} {operand_value:0>1X} | {i:0>4b} |{instruction.machine_code.to01(): <30}")
            ofile.write(f"{instruction.machine_code.to01()}\n")

print(f'{"  Done.  ":=^120}')
