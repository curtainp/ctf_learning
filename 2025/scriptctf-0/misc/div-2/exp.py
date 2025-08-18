"""
Here secret is a 128 bit length integer like this:
0b110100

we loop from 0b100000 to 0b111111 lower a bit each time:
100000
110000
111000
...

to get the div result, if result equal to 1, indicate that current bit should be set, otherwise not.
"""

from pwn import *

host = 'play.scriptsorcerers.xyz'
port = 10254

io = remote(host, port)

current = 0
for i in range(128, 0, -1):
    current += (1 << (i - 1))
    io.sendlineafter(b'Choice: ', b'1')
    io.sendlineafter(b'Enter a number: ', str(current).encode())
    res = int(io.recvline())
    if res == 1:
        continue
    else:
        # clear current bit
        current -= (1 << (i - 1))

# now current is the secret number
print(f'[+] Yeah, we get the secret number: {current}')
io.sendlineafter(b'Choice: ', b'2')
io.sendlineafter(b'Enter secret number: ', str(current).encode())

print(io.recvline())
