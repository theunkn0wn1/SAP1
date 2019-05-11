import dataclasses

from bitarray import bitarray

from .component_bases import BusComponent
from .register import Register


@dataclasses.dataclass
class ALU(BusComponent):
    """
    ALU emulation class
    """
    A_REGISTER: Register
    B_REGISTER: Register

    @property
    def value(self) -> bitarray:
        """
        Computes the current value of the ALU.

        This takes the value of :obj:`A_REGISTER` and adds the two's complement of
        :obj:`B_REGISTER`

        Notes:
            this value truncates any carry out / overflows and returns the 8 Least Significant Bits.

        Returns:
            size 8 bitarray value
        """
        # cast register A to an int
        a_value = int(self.A_REGISTER)

        computed = a_value + self.b_value
        as_bin = bin(computed)[2:]
        as_bits = bitarray(f"{as_bin:0>8}")

        return as_bits[-8:]

    @property
    def b_value(self) -> int:
        """
        returns the value of the b register, or its 2's complement if the SUB control line is high.

        Returns:
            size 8 bitarray
        """

        if not self.control_word.SUB:
            # we are not subtracting, return the state of the B register
            return int(self.B_REGISTER)

        # ### we are subtracting, compute 2's complement.

        # copy the value from the B register ( since the next methods are inplace modifies -_- )
        copy: bitarray = self.B_REGISTER.memory.copy()

        # invert the copy (!copy) (( 1's complement ))
        copy.invert()

        # we can't do math against a bitarray, so we cast it to an integer
        value = int(copy.to01(), 2)

        # add one ((2's complement ))
        value += 1

        # and now we cast it back into a bitarray

        result = bin(value)[2:]  # slice off the `0b` from the front

        result = result[-8:]  # take the last 8 bits

        # and cast back to an int
        return int(result, 2)
