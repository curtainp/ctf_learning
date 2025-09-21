from cracker import Untwister
from pwn import remote
import ast

io = remote('the-bear-cc329b4877ff901a.challs.tfcctf.com', 1337, ssl=True)

_ = io.sendlineafter(b'Enter your choice: ', b'2')
_ = io.recvuntil(b'... chat? ')

enc = ast.literal_eval(io.recvline().decode())
flag_len = len(enc)
print(f'get encode flag: {type(enc)} {enc} with {flag_len} len')

samples = []
for i in range(1600):
    _ = io.sendlineafter(b'Enter your choice: ', b'1')
    _ = io.recvuntil(b'do with it: ')
    sample = int(io.recvline().decode())
    # print(f'get sample: {sample}')
    samples.append(sample)

io.close()

print(f'get {len(samples)} samples')

ut = Untwister()
for s in samples:
    bits = f'{s:026b}'.replace('0b', '') + '?' * 6
    assert len(bits) == 32
    ut.submit(bits)
    ut.submit('?' * 32)

rnd = ut.get_random()
key = rnd.choices(list(range(256)), k = flag_len)

flag = ''.join(chr(enc[i] ^ key[i]) for i in range(flag_len))
print(flag)
