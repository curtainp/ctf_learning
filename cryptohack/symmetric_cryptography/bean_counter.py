import requests
from pwn import xor


def encrypt():
    r = requests.get("http://aes.cryptohack.org/bean_counter/encrypt/")
    return r.json()["encrypted"]


# png header first 16 bytes
png_header = bytes.fromhex("89504e470d0a1a0a0000000d49484452")
data = bytes.fromhex(encrypt())

key = xor(png_header, data[:16])
flag = xor(key, data)  # default cut = max

with open("bean_counter.png", "wb") as f:
    f.write(flag)
