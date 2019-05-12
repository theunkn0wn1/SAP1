from bitarray import bitarray

from sap1.emulator.hardware import Mar, Ram


def load_memory_from_buffer(buffer: str, mar: Mar, ram: Ram):
    lines = buffer.rstrip().split("\n")

    assert len(lines) == 16, f"memory is of an invalid size( {len(lines)}, should be exactly 16 )  "

    for i, line in enumerate(lines):
        mar.memory = bitarray(f"{i:0>4b}")
        ram.value = bitarray(line)
        assert len(ram.value) == 8, "invalid memory word!"
        print(ram.value)
