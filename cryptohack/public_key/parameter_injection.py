"""
MITM: we can forge message that send to each side.
"""

import pwn
import json
import hashlib
from Crypto.Cipher import AES

port = 13371
host = "socket.cryptohack.org"


def main():
    io = pwn.connect(host, port)
    try:
        io.recvuntil(b": ")
        line_from_alice = json.loads(io.recvline().strip().decode())
        p = int(line_from_alice["p"], 16)
        g = int(line_from_alice["g"], 16)
        A = int(line_from_alice["A"], 16)

        payload = json.dumps({"p": hex(p), "g": hex(g), "A": hex(p)})
        io.sendlineafter(b": ", payload)

        io.recvuntil(b": ")
        line_from_bob = json.loads(io.recvline().strip().decode())
        B = int(line_from_bob["B"], 16)

        payload = json.dumps({"B": hex(p)})
        io.sendlineafter(b": ", payload)

        io.recvuntil(b": ")
        result = json.loads(io.recvline().strip().decode())
        iv = bytes.fromhex(result["iv"])
        encrypted_flag = bytes.fromhex(result["encrypted_flag"])
        sha1 = hashlib.sha1()
        secret = 0
        sha1.update(str(secret).encode())
        key = sha1.digest()[:16]
        aes = AES.new(key, AES.MODE_CBC, iv)
        print(aes.decrypt(encrypted_flag))
    finally:
        io.close()


main()
