"""
Read a firmware binary and present the contained data
"""
import argparse
import functools
import itertools
import logging
import pathlib

LOG = logging.getLogger(f"mecha.{__name__}")

to_int = functools.partial(int.from_bytes, byteorder="big")

if __name__ == '__main__':
    print("firmware reading package.")

    parser = argparse.ArgumentParser("firmware reader")

    parser.add_argument("target", help="binary file to read")

    args = parser.parse_known_args()[0]

    target = pathlib.Path(args.target)

    if not target.exists() or not target.is_file():
        print(f"Target '{target.absolute()}' does not exist or  is not a file.")
        exit(2)

    print(f"reading data from {target.resolve()}...")

    counter = itertools.count()
    with target.open("rb") as ifile:
        offset = 0
        while offset <= 128:
            offset = next(counter)
            # read one byte from file
            word = ifile.read(1)
            print(f"offset: {offset:X}\tbin:={to_int(word):0>8b}\thex:=0x{to_int(word):0>2X}")
