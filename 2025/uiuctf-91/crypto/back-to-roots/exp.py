from decimal import Decimal
from random import randint
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

leak = 4336282047950153046404
original_k = 0

guess = 0
while guess != leak:
    original_k = randint(10**10, 10**11)
    guess = int(str(Decimal(original_k).sqrt()).split(".")[-1])

print(f"original: {original_k}")
