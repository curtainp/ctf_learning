from pwn import *
import codecs
import base64
import json
from Crypto.Util.number import long_to_bytes

host = 'socket.cryptohack.org'
port = 13377

io = remote(host, port)

for _ in range(100):
    resp = json.loads(io.recvline().decode())

    encoding = resp['type']
    enc = resp['encoded']

    if encoding == 'base64':
        decoded = base64.b64decode(enc.encode()).decode()
    elif encoding == 'hex':
        decoded = bytes.fromhex(enc).decode()
    elif encoding == 'rot13':
        decoded = codecs.decode(enc, 'rot13')
    elif encoding == 'bigint':
        decoded = long_to_bytes(int(enc,16)).decode()
    elif encoding == 'utf-8':
        decoded = ''.join(chr(b) for b in enc)

    input = json.dumps({'decoded': decoded})

    print(f'[+] get decode text "{decoded}" from type "{encoding}"')
    io.sendline(input.encode())

print(io.recvallS())
