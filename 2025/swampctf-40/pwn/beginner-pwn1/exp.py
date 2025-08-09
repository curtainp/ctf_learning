#!/usr/bin/env python

from pwn import *

io = remote("chals.swampctf.com", 40004)

io.sendlineafter(b'please enter your name: ', b'helloworld1')

io.sendlineafter(b'flag? (y/n) ', b'y')

io.recvuntil(b'Here is your flag! ')

flag = io.recvline()

print(flag.decode())
