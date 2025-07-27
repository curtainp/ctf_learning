from Crypto.Cipher import AES

ciphertext = bytes.fromhex(
    "41593455378fed8c3bd344827a193bde7ec2044a3f7a3ca6fb77448e9de55155"
)

from z3 import *

s = Solver()

a = Int("a")
b = Int("b")
c = Int("c")
d = Int("d")

s.add(a > 0)
s.add(a < 20000)
s.add(b > 0)
s.add(b < 20000)
s.add(c > 0)
s.add(c < 20000)
s.add(d > 0)
s.add(d < 20000)
s.add(a**4 + b**4 == c**4 + d**4 + 17)

if s.check() == sat:
    m = s.model()
    print(m[a], m[b], m[c], m[d])
else:
    print("not work")
