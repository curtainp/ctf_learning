from pwn import xor

hidden_flag = bytes.fromhex(
    "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
)

# we known first character of flag is c
favourite_byte = hidden_flag[0] ^ ord("c")

res = ""

for h in hidden_flag:
    res += chr(h ^ favourite_byte)

print(res)
