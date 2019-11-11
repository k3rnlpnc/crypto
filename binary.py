import os
import blocks


def file_to_bytes_array(path):
    """
    :param path: file we read
    :return: array of bites + size of message (file)
    """
    size = os.path.getsize(path)
    byte_array = []
    with open(path, 'rb') as f:
        while True:
            buf = f.read(8)
            if not buf:
                break
            byte_array.append(buf)
    return byte_array, size


def write_binary(path, data):
    """
    :param path: file we write
    :param data: some binary data
    """
    with open(path, 'wb') as f:
        f.write(data)


def write_text(path, data):
    with open(path, 'w') as f:
        f.write(data)


