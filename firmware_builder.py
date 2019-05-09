from sap1 import instruction_set
from sap1.instruction_set.microcode import Microcode


def fmt_table():
    header = f"{'instruction': >12}| {'step': ^5}|"
    for key in vars(Microcode()):
        header += f"{key: ^5}|"
    print(header)
    for mnemonic, instruction in instructions.items():
        print(f"{'.':.^120}")
        for i, code in enumerate(instruction.states):
            line = f"{mnemonic: >12}| {i: ^5}|"
            for bit in vars(code).values():
                line += f"{bit: ^5}|"
            print(line)


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
    instructions = {'LDA': instruction_set.lda(ptr=0),
                    'ADD': instruction_set.add(ptr=0),
                    'SUB': instruction_set.sub(ptr=0),
                    'OUT': instruction_set.out(ptr=0),
                    'JMP': instruction_set.jmp(ptr=0),
                    'HLT': instruction_set.hlt(), }

    fmt_table()

    print(f"{'  Done.  ':=^120}")
