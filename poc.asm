#  proof of concept ASM file
# function: a += b, starting from 2
# while True:
#   a += b

LDA 15  # load 0xF into A
    ADD 14   # add 0xD to A
    SUB 13  # subtract 0xC from A
    JMP 1  # while True GOTO add
 HLT # totally unreachable but whatever, probably a good thing to have