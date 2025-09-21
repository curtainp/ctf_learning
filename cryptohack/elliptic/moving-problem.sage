import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

flag = b'crypto{??????}'

def gen_keypair(G, p):
    n = random.randint(1, (p - 1))
    P = n * G
    return n, P

def gen_shared_secret(P, n):
    S = P * n
    return S.xy()[0]
    
def encrypt_flag(shared_secret: int):
    key = hashlib.sha1(str(shared_secret).encode()).digest()[:16]
    
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(flag, 16))
    
    data = {}
    data['iv'] = iv.hex()
    data['encrypte_flag'] = ciphertext.hex()
    return data
    
p = 1331169830894825846283645180581
a = -35
b = 98
E = EllipticCurve(GF(p), [a,b])
G = E.gens()[0]

# Generate keypair
n_a, P1 = gen_keypair(G, p)
n_b, P2 = gen_keypair(G, p)

# Calculate shared secret
S1 = gen_shared_secret(P1, n_b)
S2 = gen_shared_secret(P2, n_a)

# Check protocol works
assert S1 == S2

flag = encrypt_flag(S1)

print(f"Generator: {G}")
print(f"Alice Public key: {P1}")
print(f"Bob Public key: {P2}")
print(f"Encrypted flag: {flag}")
    
