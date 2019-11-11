import argparse
import hash as HASH
import feistel


def commandline_parser():
    parser = argparse.ArgumentParser()
    # password's size
    parser.add_argument('-s', '--size', nargs='?', default="8")
    parser.add_argument('-f', '--file', nargs='?', default='table.hsh')
    return parser


def main():
    parser = commandline_parser()
    namespace = parser.parse_args()

    size = int(namespace.size)
    dict_len = len(HASH.Hash.DICTIONARY)
    length_chain = 100
    N = 1000
    password = ''
    f = open(namespace.file, 'aw')
    hash = HASH.Hash(password, '25470023', 10, 10, feistel.Feistel, 8, 8)
    for i in range(N):
        password = HASH.new_pass(size, HASH.Hash.DICTIONARY)
        f.write(password + ' => ')
        for n in range(length_chain):
            if n % 2:
                password = HASH.reduce(password, n)
                f.write(password + ' => ')
            else:
                password = hash.hash()
                f.write(password + ' => ')
        f.write('\n')
    f.close()


if __name__ == '__main__':
    main()