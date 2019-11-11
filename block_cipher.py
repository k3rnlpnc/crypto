import argparse
import sys
import binary
import blocks
import feistel
import operations


def commandline_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', nargs='?', default="d")
    parser.add_argument('-v', '--vect', nargs='?', default="")
    parser.add_argument('-k', '--key', nargs='?', default="2548716611457336")
    parser.add_argument('-n', '--numrnd', nargs='?', default="6")
    parser.add_argument('-r', '--rfile', nargs='?', default="ciphertext.txt")
    parser.add_argument('-w', '--wfile', nargs='?', default="decdoc.txt")
    return parser


def main():
    parser = commandline_parser()
    namespace = parser.parse_args()

    blocks, size_of_file = binary.file_to_bytes_array(namespace.rfile)
    close_key = bytes(namespace.key, encoding='utf-8')
    init_vector = bytes(namespace.vect, encoding='utf-8')
    algo = feistel.Feistel(blocks, close_key, 8, int(namespace.numrnd), size_of_file, init_vector)
    if (namespace.mode == 'e'):
        binary.write_binary(namespace.wfile, algo.encrypt_data(init_vector))
    elif (namespace.mode == 'd'):
        binary.write_binary(namespace.wfile, algo.decrypt_data(init_vector))

if __name__ == '__main__':
    main()