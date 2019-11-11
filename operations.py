def rol(val, r_bits, length):
    """ Сyclic left shift of a sequence of bytes """
    return (val << r_bits % length) & (2 ** length - 1) | (val & (2 ** length - 1)) >> (length - (r_bits % length))


def ror(val, r_bits, length):
    """ Cyclic right shift of a sequence of bytes """
    return ((val & (2**length-1)) >> r_bits%length) | (val << (length-(r_bits%length)) & (2**length-1))


def get_uneven_bits(integer):
    uneven = ''
    if not integer.bit_length() % 2:
        integer >>= 1
    while integer:
        uneven += str(integer & 1)
        integer >>= 2
    if uneven:
        return int(uneven[::-1], 2)
    else:
        return 0