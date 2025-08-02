"""
Intercepted from Alice: {"supported": ["DH1536", "DH1024", "DH512", "DH256", "DH128", "DH64"]}
Send to Bob: {"supported":["DH64"]}
Intercepted from Bob: {"chosen": "DH64"}
Send to Alice: {"chosen": "DH64"}
Intercepted from Alice: {"p": "0xde26ab651b92a129", "g": "0x2", "A": "0xb53436559c3dded0"}
Intercepted from Bob: {"B": "0xd451b8b0d112301b"}
Intercepted from Alice: {"iv": "4a7988f2e78913ab5828e10dd0721970", "encrypted_flag": "d68d7691fb480a85f3d30e83f80404bf2cd2e246f3608f5c88320d3da6a8af42"}
"""

p = int("0xde26ab651b92a129", 16)
g = 2
A = int("0xb53436559c3dded0", 16)
B = int("0xd451b8b0d112301b", 16)
iv = bytes.fromhex("4a7988f2e78913ab5828e10dd0721970")
encrypted_flag = bytes.fromhex(
    "d68d7691fb480a85f3d30e83f80404bf2cd2e246f3608f5c88320d3da6a8af42"
)

import hashlib
from Crypto.Cipher import AES

a = 3535373327163069102
secret = pow(B, a, p)

sha1 = hashlib.sha1()
sha1.update(str(secret).encode())
key = sha1.digest()[:16]
aes = AES.new(key, AES.MODE_CBC, iv)
print(aes.decrypt(encrypted_flag))
