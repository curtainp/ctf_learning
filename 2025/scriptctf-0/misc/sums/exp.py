from pwn import *

host = 'play.scriptsorcerers.xyz'
port = 10474

io = remote(host, port)

n = 123456

nums = list(map(int, io.readline().split(b' ')))

rngs = []
for _ in range(n):
    l, r = map(int, io.readline().split(b' '))
    rngs.append((l, r))

# we need to solve the sum with external program, because Python is slow.
for i in range(n):
    # res = 0
    # l, r = rngs[i]
    # for j in range(l, r + 1):
    #     res += nums[j]

    # if i % 1000 == 0:
    #     print(f'push res: {res}')
    io.sendline(str(res).encode())

print(io.recvline())
