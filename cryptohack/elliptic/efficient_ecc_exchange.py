from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
from point_multiplication import scalar_multiplication

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

def decrypt_flag(shared_secret:int, iv: str, ciphertext: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')


a = 497
b = 1768
p = 9739

Qx = 4726
Qy_2 = Qx**3 + a * Qx + b
# thanks p === 3 mod 4, refer quadratic residue and legendre symbol
assert pow(Qy_2, ((p - 1) // 2), p) == 1
Qy = pow(Qy_2, ((p + 1) // 4), p)
Q = (Qx, Qy)
nb = 6534
S = scalar_multiplication(Q, nb, a, p)
shared_secret = S[0]
iv = 'cd9da9f1c60925922377ea952afc212c'
ciphertext = 'febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8'

print(decrypt_flag(shared_secret, iv, ciphertext))
