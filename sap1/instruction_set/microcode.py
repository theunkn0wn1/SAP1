from dataclasses import dataclass

from bitarray import bitarray

from .types import Bit


@dataclass(frozen=True)
class Microcode:
    """
    Represents a microcode instruction
    """
    HLT: Bit = Bit(0)  # halt
    MI: Bit = Bit(0)  # Mar write enable
    RI: Bit = Bit(0)  # Ram write enable
    RO: Bit = Bit(0)  # Ram read enable
    IO: Bit = Bit(0)  # instruction register read enable
    II: Bit = Bit(0)  # instruction register write enable
    AI: Bit = Bit(0)  # accumulator write enable
    AO: Bit = Bit(0)  # accumulator read enable
    EpsilonOut: Bit = Bit(0)  # ALU read enable
    SUB: Bit = Bit(0)  # ALU subtract flag
    BI: Bit = Bit(0)  # B register write enable
    BO: Bit = Bit(0)  # B register read enable
    OI: Bit = Bit(0)  # Output register enable
    CE: Bit = Bit(0)  # PC enable
    OC: Bit = Bit(0)  # ???
    JMP: Bit = Bit(0)  # PC write enable (jump)

    def dump(self) -> bitarray:
        """
        Dump this microcode instruction to a bit array

        Returns:
            (bitarray) array of bits
        """
        buffer = bitarray()
        buffer.append(self.HLT)
        buffer.append(self.MI)
        buffer.append(self.RI)
        buffer.append(self.RO)
        buffer.append(self.IO)
        buffer.append(self.II)
        buffer.append(self.AI)

        buffer.append(self.AO)
        buffer.append(self.EpsilonOut)
        buffer.append(self.SUB)
        buffer.append(self.BI)
        buffer.append(self.BO)
        buffer.append(self.OI)
        buffer.append(self.CE)
        buffer.append(self.OC)
        buffer.append(self.JMP)

        return buffer


NO_OP = Microcode()
