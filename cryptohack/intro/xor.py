from pwn import *

flag = "".join(chr(13 ^ ord(e)) for e in "label")
flag2 = xor(b"label", 13)

print(flag, flag2)
