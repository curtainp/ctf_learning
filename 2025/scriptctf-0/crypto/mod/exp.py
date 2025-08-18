from pwn import *

host = 'play.scriptsorcerers.xyz'
port = 10131

io = remote(host, port)

# os.urandom(32) will get a 256 bit length integer
mask = 2**256 - 1

io.sendlineafter(b'Provide a number: ', str(mask).encode())

res = int(io.recvline().strip())

# modulo will get a integer that with bit set which not in secret
secret = mask - res

io.sendlineafter(b'Guess: ', str(secret).encode())

print(io.recvline())
