import argparse
import typing

from sap1 import instruction_set
from sap1.compiler.word import Word, address
from sap1.instruction_set.microcode import Microcode


def table_human_dump():
    """
    Dump all the words into a human-readable table
    Returns:

    """
    print(f"{'Truth Table':-^120}")
    header = f"{'instruction': >12}| {'opcode': ^6}| {'t': ^3}|"
    for key in vars(Microcode()):
        header += f"{key: ^5}|"

    print(header)
    for mnemonic, instruction in instructions.items():
        print(f"{'.':.^120}")
        for i, code in enumerate(instruction.states):
            line = f"{mnemonic: >12}| {instruction.opcode.to01(): ^6}| {i:0>3b}|"  # FIXME check what max T should be in binary
            # dump the microcode word to binary for rendering
            for bit in code.dump().to01():
                line += f"{bit: ^5}|"

            print(line)


def table_human_hex():
    """
    dump instructions into a human_readable
    Returns:

    """
    print(f"{'Word table':-^120}")
    header = f"{'mnemonic': >12}| {'t': ^3}| {'address': ^9}| {'word': ^20} |"

    print (header)
    for mnemonic, instruction in instructions.items():
        print(f"{'.':.^120}")
        for i, code in enumerate(instruction.states):
            addr = address(instruction, i)
            word = Word(address=addr, code=instruction.states[i])
            line = f"{mnemonic: >12}| {i: ^3}| {addr.to01(): ^9}| {word.word.to01(): ^20} |"

            print(line)




def table_hex() -> typing.Dict:
    ...


if __name__ == '__main__':
    print(r"""
 _____  ___  ______       __   ______ ______________  ____    _  ___  ______ _____
/  ___|/ _ \ | ___ \     /  |  |  ___|_   _| ___ \  \/  | |  | |/ _ \ | ___ \  ___|
\ `--./ /_\ \| |_/ /_____`| |  | |_    | | | |_/ / .  . | |  | / /_\ \| |_/ / |__
 `--. \  _  ||  __/______|| |  |  _|   | | |    /| |\/| | |/\| |  _  ||    /|  __|
/\__/ / | | || |         _| |_ | |    _| |_| |\ \| |  | \  /\  / | | || |\ \| |___
\____/\_| |_/\_|         \___/ \_|    \___/\_| \_\_|  |_/\/  \/\_| |_/\_| \_\____/


______ _   _ _____ _    ______ ___________
| ___ \ | | |_   _| |   |  _  \  ___| ___ \
| |_/ / | | | | | | |   | | | | |__ | |_/ /
| ___ \ | | | | | | |   | | | |  __||    /
| |_/ / |_| |_| |_| |___| |/ /| |___| |\ \
\____/ \___/ \___/\_____/___/ \____/\_| \_|

    """)
    print(f"{'  SAP-1 Firmware Builder by Joshua (Theunkn0wn1) Salzedo  ':-^120}")
    parser = argparse.ArgumentParser("SAP-1 Firmware Builder")
    parser.add_argument("--truth-table", action="store_true",
                        help="display a human-readable truth table of firmware package")
    parser.add_argument("--word-table", action="store_true")
    args = parser.parse_args()
    instructions = {'LDA': instruction_set.lda(ptr=0),
                    'ADD': instruction_set.add(ptr=0),
                    'SUB': instruction_set.sub(ptr=0),
                    'OUT': instruction_set.out(ptr=0),
                    'JMP': instruction_set.jmp(ptr=0),
                    'HLT': instruction_set.hlt(), }
    if args.truth_table:
        table_human_dump()

    if args.word_table:
        table_human_hex()

    print(f"{'  Done.  ':=^120}")
