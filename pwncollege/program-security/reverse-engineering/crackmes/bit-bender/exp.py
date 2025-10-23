from pwn import *

context.binary = elf = ELF('/challenge/bit-bender', checksec=False)

io = elf.process()

final_key = 'VLFDYyhuaVqbRBTY'

'''
for ( i = 0; i < 0x10; ++i )
      final_key[i] = ((input[i] + 123) >> 4) | (16 * (input[i] + 123));

1. let temp = input[i] + 123
2. final_key[i] = (temp >> 4) | (temp << 4)

this swap the nibbles of temp, so reverse nibble back then subtract 123 will get the original input
'''

input_array = []
for encrypt in final_key:
    encrypt_byte = ord(encrypt)
    temp = ((encrypt_byte & 0x0f) << 4) | ((encrypt_byte & 0xf0) >> 4)
    input_array.append((temp - 123) & 0xff)

print(f'bytes: {bytes(input_array)}')

assert len(input_array) == 16, "length of key must be 16"

io.sendline(bytes(input_array))

io.interactive()
