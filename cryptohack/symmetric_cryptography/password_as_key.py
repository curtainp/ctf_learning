from Crypto.Cipher import AES
import hashlib

with open("words.txt") as f:
    words = [w.strip() for w in f.readlines()]


def decrypt(ciphertext, key):
    ciphertext = bytes.fromhex(ciphertext)

    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return b''

    return decrypted

ciphertext = 'c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66'
for w in words:
    key = hashlib.md5(w.encode()).digest()
    plaintext = decrypt(ciphertext, key)
    if b'crypto{' in plaintext:
        print(plaintext)
        exit(0)
        



