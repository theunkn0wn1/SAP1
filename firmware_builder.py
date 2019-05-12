import argparse
import io
import pathlib
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


def table_words() -> typing.List[typing.BinaryIO]:
    """
    dump instructions into a human_readable
    Returns:

    """

    print(f"{'Word table':-^120}")
    header = f"{'mnemonic': >12}| {'t': ^3}| {'address': ^9}| {'EEPROM 0': ^10}| {'EEPROM 1': ^10} |"
    # create a bytesIO object to write into
    ostreams = [io.BytesIO(), io.BytesIO()]

    print(header)
    for mnemonic, instruction in instructions.items():
        print(f"{'.':.^120}")
        for i, code in enumerate(instruction.states):
            addr = address(instruction, i)
            word = Word(address=addr, code=instruction.states[i])
            word_as_bin = word.word.to01()
            eeprom = [word_as_bin[:8], word_as_bin[8:]]

            line = f"{mnemonic: >12}| {i: ^3}| {(int(addr.to01(), 2)):0>8b}| {eeprom[0]: ^10}| " \
                f"{eeprom[1]: ^10} |"

            print(line)
            # convert addr to integer
            raw_addr = int(addr.to01(), 2)
            # seek to specified address
            ostreams[0].seek(raw_addr)
            ostreams[1].seek(raw_addr)
            # write EEPROM data to ostreams
            ostreams[0].write(word.word[0:8])
            ostreams[1].write(word.word[8:])

    return ostreams


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
    parser.add_argument("--output", help="directory to output computed firmware binaries ",
                        default=...)
    args = parser.parse_known_args()[0]
    instructions = {'LDA': instruction_set.lda(ptr=0),
                    'ADD': instruction_set.add(ptr=0),
                    'SUB': instruction_set.sub(ptr=0),
                    'OUT': instruction_set.out(ptr=0),
                    'JMP': instruction_set.jmp(ptr=0),
                    'HLT': instruction_set.hlt(), }

    path = None
    if args.output is not ...:
        path = pathlib.Path(args.output)
        print(f"{'Output':-^120}")
        if not path.exists() or not path.is_dir():
            print(f"'{path.resolve()}' does not exist or does not point to a directory")
            exit(1)

    if args.truth_table:
        table_human_dump()

    if args.word_table:
        eeprom_a, eeprom_b = table_words()
        if path:
            print(f"using '{path.resolve()}'for output....")
            print("dumping words to binary...")
            (path / "eeprom_a.bin").write_bytes(eeprom_a.getvalue())
            (path / "eeprom_b.bin").write_bytes(eeprom_b.getvalue())

    print(f"{'  Done.  ':=^120}")
