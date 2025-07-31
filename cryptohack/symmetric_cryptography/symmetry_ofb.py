"""
OFB turn AES to stream cipher which don't require padding anymore, and the challenge provide two encrypt procedure, the second one can
used for probe the flag
"""

import requests
import string

alphabet = (
    "{"
    + "}"
    + "_"
    + "!"
    + "@"
    + string.digits
    + string.ascii_lowercase
    + string.ascii_uppercase
).encode()


def encrypt_flag() -> str:
    r = requests.get("http://aes.cryptohack.org/symmetry/encrypt_flag")
    return r.json()["ciphertext"]


def encrypt(plaintext: str, iv: str) -> str:
    r = requests.get(f"http://aes.cryptohack.org/symmetry/encrypt/{plaintext}/{iv}/")
    return r.json()["ciphertext"]


data = encrypt_flag()
iv = data[:32]

flag_cipher = data[32:]

flag = b""

while True:
    if flag.endswith(b"}"):
        break
    for c in alphabet:
        ct = encrypt(flag.hex() + hex(c)[2:], iv)
        if flag_cipher.startswith(ct):
            flag += chr(c).encode()
            print(f"probe successful for: {chr(c)}, current flag: {flag}")
            break


print(flag)
