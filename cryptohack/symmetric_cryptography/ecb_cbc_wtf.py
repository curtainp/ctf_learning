"""
CBC and ECB mode have almost similar decrypt procedure expect that CBC need one more XOR step.
this challenge give us `iv` and two ciphertext block. so:
1. plaintext1 = decrypt(ciphertext1, ECB) ^ iv
2. plaintext2 = decrypt(ciphertext2, ECB) ^ ciphertext1
"""

from pwn import xor  # for xor with bytes
import requests

iv = "6a6f41a79ac2ee2265ed3173a6375645"
ciphertext1 = "ba0ec4bac7cce369caee93468c74a63c"
ciphertext2 = "ecfe208d412e62c64c64c496dd6f9f1c"


def decrypt(ciphertext: str) -> bytes:
    r = requests.get(f"http://aes.cryptohack.org/ecbcbcwtf/decrypt/{ciphertext}/")
    return bytes.fromhex(r.json()["plaintext"])


def main():
    res = b""
    res += xor(decrypt(ciphertext1), bytes.fromhex(iv))
    res += xor(decrypt(ciphertext2), bytes.fromhex(ciphertext1))

    print(res)


if __name__ == "__main__":
    main()
