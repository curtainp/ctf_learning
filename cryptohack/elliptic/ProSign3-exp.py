from pwn import remote
import json, hashlib
from Crypto.Util.number import inverse, bytes_to_long
from ecdsa.ecdsa import generator_192

'''
there is a vulnerability within sign_time which use a `shadow varible` n that is a seconds

and luckily, the seconds is 0-59, we can brute-force to get the private key
'''

N = generator_192.order()

def sha1_long(m: bytes) -> int:
    return bytes_to_long(hashlib.sha1(m).digest())

def bruteforce_privkey(r: int, s: int, h: int, max_secs: int) -> int:
    for k in range(1, max_secs):
        if (generator_192 * k).x() % N == r:
            return (s * k - h) * inverse(r, N) % N
    raise ValueError('Could not brute force privkey!')

def sign_msg(msg: str, d: int, k: int) -> (int, int):
    h = sha1_long(msg.encode())
    r = (generator_192 * k).x() % N
    s = (inverse(k, N) * (h + d * r)) % N
    return r, s

io = remote('socket.cryptohack.org', 13381)
print(io.recvline().decode())

io.sendline(json.dumps({'option': 'sign_time'}).encode())
response = json.loads(io.recvline().decode())
msg, r, s = response['msg'], int(response['r'], 16), int(response['s'], 16)
_, time_str = msg.split(' is ')
secs = int(time_str.split(':')[1])
h = sha1_long(msg.encode())
d = bruteforce_privkey(r, s, h, secs)
print(f'[+] Recovered d = {hex(d)}')

r_new, s_new = sign_msg('unlock', d, k=2) # random choice between [1, N - 1]
payload = {
    'option': 'verify',
    'msg': 'unlock',
    'r': hex(r_new),
    's': hex(s_new)
}
io.sendline(json.dumps(payload).encode())
print(io.recvline().decode())


