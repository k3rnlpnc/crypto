import blocks
import operations
import random


class Hash:
    NUM_CODE = [i for i in range(47, 58)]
    LATIN_CODE1 = [i for i in range(64, 91)]
    LATIN_CODE2 = [i for i in range(96, 123)]
    DICTIONARY = NUM_CODE + LATIN_CODE1 + LATIN_CODE2

    def __init__(self, blocks, init_vector, iterations, num_rounds, compression_function, output_size, input_size):
        self.blocks = blocks
        self.h0 = init_vector
        self.C = iterations
        self.num_rounds = num_rounds
        self.F = compression_function
        self.size = output_size
        self.init_size = input_size
        self.b_size = 8
        self.hsh = ''

    def hash(self):
        H = self.h0
        for block in self.blocks:
            if len(block) < self.b_size:
                block = blocks.s_complete(block, self.b_size, self.init_size)
                if len(block) == 2:
                    self.blocks.append(block[1])
                    block = block[0]
            f = self.F(block, self.b_size, self.num_rounds, self.init_size)
            H = f.encrypt_block(H)
            del f
        self.hsh = format('%02x' % int.from_bytes(H, byteorder='big'))
        return self.hsh

    @staticmethod
    def static_hash(init_vector, message, size_b, F, message_size, F_rounds):
        H = init_vector
        for block in message:
            if len(block) < size_b:
                block = blocks.s_complete(block, size_b, message_size)
                if len(block) == 2:
                    message.append(block[1])
                    block = block[0]
            f = F(block, size_b, F_rounds, message_size)
            H = f.encrypt_block(H)
            del f
        hsh = format('%02x' % int.from_bytes(H, byteorder='big'))
        return hsh

    def find_collision(self):
        find = True
        i = 0
        while find:
            message = new_pass(self.size, Hash.DICTIONARY)
            message = [message[x:x+8] for x in range (0, len(message), 8)]
            hash = self.static_hash()
            if hash == self.hsh:
                find = False
            else:
                i += 1
        return i


def reduce(hash, iteration):
    hash = int(hash, 16)
    codes = list(operations.rol(hash, iteration, hash.bit_length()).to_bytes(8, byteorder='big'))
    printed_chars = ''
    while codes:
        for i in range(len(codes)):
            if codes[i] not in Hash.DICTIONARY:
                if codes[i] > 122:
                    codes[i] -= 10
                elif codes[i] < 48:
                    codes[i] += 5
                else:
                    codes[i] += 13
            else:
                printed_chars += chr(codes[i])
                del codes[i]
                break
    return printed_chars


def new_pass(size, alphabet):
    password = ''
    rnd = random.randint(0, len(alphabet))
    for i in range(size):
        password += chr(alphabet[rnd])
    return password
