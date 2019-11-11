import blocks
import operations
import binary


class Feistel:
    init_vector = 0
    close_key = 0
    round_keys = []
    init_length = 0
    size_of_block = 0
    num_rounds = 0

    def __init__(self, close_key, size_of_block, num_rounds, size_of_file, init_vector=b'', blocks=[]):
        self.blocks = blocks
        self.init_vector = int.from_bytes(init_vector, byteorder='big')
        self.close_key = int.from_bytes(close_key, byteorder='big')
        self.size_of_block = size_of_block
        # self.init_length = len(blocks)*size_of_block - (size_of_block-len(blocks[len(blocks)-1]))
        self.init_length = size_of_file
        self.num_rounds = num_rounds
        self.set_round_keys()

    def set_round_keys(self):
        for i in range(self.num_rounds):
            self.round_keys.append(self.round_key(i))

    def round_key(self, r):
        return operations.get_uneven_bits(operations.rol(self.close_key, r*9, 64))

    def F(self, sub_block):
        """ Get tmp sub-block (4b integer)
            Return new sub-block (4b integer) """
        left = sub_block >> 16
        right = sub_block & 0xffff
        return operations.rol((~left), 5, 16) << 16 | operations.ror(right, 7, 16)

    @staticmethod
    def del_junk(text):
        while True:
            if (text[-1:] == b'\x00'):
                text = text[:-1]
            else:
                break
        return text

    '''@staticmethod
    def encrypt(block, key, num_rounds):
        left = int.from_bytes(block[:4], byteorder='big')
        right = int.from_bytes(block[4:], byteorder='big')
        for i in range(num_rounds):
'''

    def encrypt_block(self, block):
        left = int.from_bytes(block[:4], byteorder='big')
        right = int.from_bytes(block[4:], byteorder='big')
        for i in range(self.num_rounds):
            tmp = right ^ self.round_keys[i]
            right = left ^ self.F(tmp)
            left = tmp
        return (left << 32 | right).to_bytes(8, byteorder='big')

    def encrypt_data(self, init_vect):
        ciphertext = b''
        cbc = init_vect
        for block in self.blocks:
            if (len(block) < 8):
                block = blocks.complete(block, 8)
            block = int.from_bytes(block, byteorder='big') ^ cbc
            block = block.to_bytes(8, byteorder='big')
            new_block = self.encrypt_block(block)
            ciphertext += new_block
            cbc = int.from_bytes(new_block, byteorder='big')
        del self.close_key
        return Feistel.del_junk(ciphertext)

    def decrypt_block(self, block):
        left = int.from_bytes(block[:4], byteorder='big')
        right = int.from_bytes(block[4:], byteorder='big')
        for i in range(self.num_rounds):
            tmp = left ^ self.round_keys[i]
            left = right ^ self.F(left)
            right = tmp
        return (left << 32 | right).to_bytes(8, byteorder='big')

    def decrypt_data(self, init_vect):
        self.round_keys.reverse()
        plaintext = b''
        for block in self.blocks:
            if (len(block) < 8):
                block = blocks.complete(block, 8)
            cbc = int.from_bytes(block, byteorder='big')
            new_block = int.from_bytes(self.decrypt_block(block), byteorder='big') ^ init_vect
            plaintext += new_block.to_bytes(8, byteorder='big')
            init_vect = cbc
        del self.close_key
        return Feistel.del_junk(plaintext)
