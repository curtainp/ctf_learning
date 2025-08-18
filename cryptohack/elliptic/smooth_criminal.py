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
