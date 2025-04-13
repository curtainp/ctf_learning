import string
from pwn import *

context.log_level = 'debug'
MAX_FLAG_LEN = 128

# io = process("./chal_local.py")
# io = remote("challenge.utctf.live", 7150)

'''
make_plaintext ensure that our prefix is push at beginning of the secret:
    chksum = sum(ord(c) for c in x ) % (len(x) + 1)
    assert(chksum == len(x))
'''

def make_plaintext(prefix):
    attempt = 0
    x = prefix
    while True:
        if sum(ord(c) for c in x) % (len(x) + 1) == len(prefix):
            return x
        x = prefix + string.ascii_letters[attempt]
        attempt += 1

def ecb_byte_at_a_time(known_pt = ""):
    known_pt = ("A" * 16) + known_pt

    alphabet = string.ascii_letters + string.digits + "_!?{}"

    def read_ct():
        ct = int(io.readline().decode(), 16)
        ct = ct.to_bytes(length=(ct.bit_length() + 7) // 8, byteorder='big')
        return ct

    for i in range(MAX_FLAG_LEN):
        padding = 15 - (i % 16)
        pt = make_plaintext("A" * padding)
        io.sendlineafter(b"to be encrypted: ", pt.encode())
        ct = read_ct()

        dict_cts = {}
        for c in alphabet:
            dict_known_pt = known_pt[len(known_pt) - 16 + 1: len(known_pt)]
            dict_pt = make_plaintext(dict_known_pt + c)

count = 11
for i in string.printable:
    x = i * count
    chksum = sum(ord(c) for c in x) % (len(x) + 1)
    if chksum == count:
        print(f"using {x}")
        break
