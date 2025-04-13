# RSA algorithm concepts:
# public key and private key
# (e, n)           (d, n)
# 
# Steps in RSA algorithm
# 1. key generation:
#     - choose two distinct large prime number p and q
#     - compute n = p x q. this is the modulus for both the public and private keys
#     - compute Euler's totient function phi(n) = (q - 1) x (p - 1)
#     - choose a integer e such that:
#       - 1 < e < phi(n)
#       - gcd(e, phi(n)) = 1 (e and phi(n) are coprime)
#       - commonly, e = 65537 is used because its a prime number and efficient for computation
#     - compute d, the modular multiplicative inverse of e modulo phi(n)
#       - d x e === 1 mod phi(n)
# 2. encryption
#   c = m ^ e mod n
# 3. decryption
#   m = c ^ d mod n

# solution
the description hint that `n` is made using only one prime.
