#! /usr/bin/env python3


'''
basewhite.py
Translate binary data to an encoding optimized for printing.
'''


from sys import argv, stdin, stdout


CHARACTERS = [
    ord('\t'),
    ord('\r'),
    ord('\n'),
    ord(' ')
]


def encode_byte(b: int) -> bytes:
    ''' Encode the single byte ``b`` to basewhite bytes. Each byte
    gets turned to four bytes in basewehite encoding. '''

    digits = [
        CHARACTERS[b & 0b00000011],
        CHARACTERS[(b & 0b00001100) >> 2],
        CHARACTERS[(b & 0b00110000) >> 4],
        CHARACTERS[(b & 0b11000000) >> 6]
    ]

    return bytes(digits)


def decode_quadruplet(q: bytes) -> int:
    ''' Decode q[4] back to a regular byte. '''

    res = 0

    for i in range(4):
        res += (CHARACTERS.index(q[i]) << (2 * i))

    return res


def encode():
    c = stdin.buffer.read(1)

    while c != b'':
        encoded = encode_byte(c[0])
        stdout.buffer.write(encoded)

        if c == ord('\n'):
            stdout.flush()

        c = stdin.buffer.read(1)


def decode():
    c = stdin.buffer.read(4)
    while c != b'' and len(c) == 4:
        decoded = decode_quadruplet(c)
        stdout.buffer.write(bytes([decoded]))

        if decoded == ord('\n'):
            stdout.flush()

        c = stdin.buffer.read(4)


def main():
    if '-d' in argv:
        decode()
    else:
        encode()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
