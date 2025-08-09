"""
ECDLP: elliptic curve discrete logarithm problem of finding an integer n such that Q = n*P

use Elliptic Curve for Diffie-Hellman key exchange goes as follow:
* alice generates a secret random integer n_a and calculates Qa = n_a * G
* bob generates a secret random integer n_b and calculates Qb = n_b * G
* exchange each other's Qa and Qb
* due to the associativity of scalar multiplication, the shared secret is: S = n_a * Qb = n_b * Qa
"""

from point_multiplication import scalar_multiplication
from Crypto.Util.number import long_to_bytes
import hashlib

a = 497
p = 9739
Qa = (815, 3190)
nb = 1829

S = scalar_multiplication(Qa, nb, a, p)
# print(S)
sha = hashlib.sha1()
sha.update(str(S[0]).encode())
flag = sha.digest().hex()
print(flag)
