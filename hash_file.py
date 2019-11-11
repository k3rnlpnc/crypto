import argparse
import binary
import feistel
import hash


def commandline_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vect', nargs='?', default="somevalue")
    parser.add_argument('-n', '--rounds', nargs='?', default="6")
    parser.add_argument('-i', '--iterations', nargs='?', default="6")
    parser.add_argument('-s', '--size', nargs='?', default="64")
    parser.add_argument('-r', '--rfile', nargs='?', default="name.txt")
    parser.add_argument('-w', '--wfile', nargs='?', default="hash.hsh")
    return parser


def main():
    parser = commandline_parser()
    namespace = parser.parse_args()

    blocks, size_of_file = binary.file_to_bytes_array(namespace.rfile)
    init_vector = bytes(namespace.vect, encoding='utf-8')
    algo = hash.Hash(blocks, init_vector, int(namespace.rounds), int(namespace.iterations), feistel.Feistel, int(namespace.size), size_of_file)

    digest = algo.hash()
    # collision = algo.find_collision()
    print(digest)
    binary.write_text(namespace.wfile, digest)

if __name__ == '__main__':
    main()