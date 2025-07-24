"""
extend Euclidean algorithm is an efficient way to find the integers `u`, `v` such that:
a * u + b * v = gcd(a, b)
when a and b is prime, the equation right equal to 1.

au + bv = gcd(b, a % b)
        = bu1 + (a % b)v1
        = bu1 + (a - (a // b) * b)v1
        = av1 + b(u1 - (a // b)v1)

so:
    u = v1
    v = u1 - (a // b) *  v1
"""


def ext_gcd(a, b):
    if b == 0:
        return 1, 0
    else:
        x, y = ext_gcd(b, a % b)
        return y, x - (a // b) * y


print(ext_gcd(26513, 32321))
