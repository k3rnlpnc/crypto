def z_complete(data, size):
    """Get bytes
        Return byte sequence 8b size """
    diff = size - len(data)
    data += b'\x00' * diff
    return data

def s_complete(data, size, msg_size):
    """Get bytes < size
        Return bytes with trash -> length of message + zero bytes"""
    diff = size - len(data)
    salt_size = msg_size.bit_length() // 8 + 1
    if (diff < salt_size):
        added_data = msg_size.to_bytes(size, byteorder='little')
        data += b'\x00' * diff
        return data, added_data
    else:
        data += msg_size.to_bytes(diff, byteorder='little')
        return data

