from pwn import xor

hidden_flag = bytes.fromhex(
    "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
)

known_prefix = b"crypto{"

secret_keys = xor(hidden_flag, known_prefix, cut="min")

# after this we can get the secret key is: myXORke
# so we guess that key is: myXORkey

secret_keys += b"y"

flag = xor(hidden_flag, secret_keys)

print(flag.decode())
