from re import finditer
from Crypto.Cipher import AES
from Crypto.Util.number import inverse
from Crypto.Util.Padding import pad, unpad
from collections import namedtuple
from random import randint
import hashlib
import os

# Create a simple Point class to represent the affine points.
Point = namedtuple("Point", "x, y")

# The point at infinity (origin for the group law)
O = "Origin"

flag = b'crypto{xxxxxxxx}'

def check_point(P: tuple):
    if P == O:
        return true
    else:
        return (P.y**2 - (P.x**3 + a*P.x + b)) % p == 0 and 0 <= P.x < p and 0 <= P.y < p

def point_inverse(P: tuple):
    if P == O:
        return P
    return Point(P.x, -P.y % p)

def point_addition(P: tuple, Q: tuple):
    # based of algo, in ICN
    if P == O:
        return Q
    elif Q == O:
        return P
    elif Q == point_inverse(P):
        return O
    else:
        if P == Q:
            lam = (3*P.x**2 + a) * inverse(2*P.y, p)
            lam %= p
        else:
            lam = (Q.y - P.y) * inverse((Q.x - P.x), p)
            lam %= p

        Rx = (lam**2 - P.x - Q.x) % p
        Ry = (lam * (P.x - Rx) - P.y) % p
        R = Point(Rx, Ry)
        assert check_point(R)
        return R

def double_and_add(P: tuple, n: int):
    Q = P
    R = O
    while n > 0:
        if n % 2 == 1:
            R = point_addition(R, Q)
        Q = point_addition(Q,Q)
        n = n // 2
    assert check_point(R)
    return R

def gen_shared_secret(Q: tuple, n: int):
    S = double_and_add(Q, n)
    return S.x

def encrypt_flag(shared_secret: int):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(flag, 16))
    data = {}
    data['iv'] = iv.hex()
    data['encrypted_flag'] = ciphertext.hex()
    return data

def decrypt_flag(shared_secret: int, iv: str, encrypted: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]

    biv = bytes.fromhex(iv)
    bencrypted = bytes.fromhex(encrypted)

    cipher = AES.new(key, AES.MODE_CBC, biv)
    return cipher.decrypt(bencrypted)

# Define the curve
p = 310717010502520989590157367261876774703
a = 2
b = 3

# Generator
g_x = 179210853392303317793440285562762725654
g_y = 105268671499942631758568591033409611165
# G = Point(g_x, g_y)

# # My secret int, different every time!!                
# n = randint(1, p)

# # Send this to Bob!
# public = double_and_add(G, n)
# print(public)

# # Bob's public key
# b_x = 272640099140026426377756188075937988094
# b_y = 51062462309521034358726608268084433317
# B = Point(b_x, b_y)

# # Calculate Shared Secret
# shared_secret = gen_shared_secret(B, n)

# # Send this to Bob!
# ciphertext = encrypt_flag(shared_secret)
# print(ciphertext)

# with sage we use Pohlig-Hellman algorithm for solve discrete logarithm
# y^2 = x^3 + a * x + b
E = EllipticCurve(GF(p), [a, b])

# 1. define point G, A, B with E(xxx, xxx)
# 2. compute private key with G.discrete_log(A) => a which is private key of A, the same as the other
# 3. the shared_secret = (A * b) or (B * a) 
