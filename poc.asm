#  proof of concept ASM file
# function: a += b, starting from 2
# while True:
#   a += b

LDA 15  # load 0xF into A
    ADD E   # add 0xD to A
    SUB D  # subtract 0xC from A
    OUT  # emit value to output
    JMP 1  # while True GOTO add
 HLT # totally unreachable but whatever, probably a good thing to have