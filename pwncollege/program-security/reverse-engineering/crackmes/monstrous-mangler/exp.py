from pwn import *
import sys

if len(sys.argv) != 2:
    print(f'[x] Usages: {sys.argv[0]} [challenge_mode]')
    print(f'\t[example]{sys.argv[0]} easy\t\t\t will trigger easy mode challenge exp.')
    exit(1)

assert sys.argv[1] == 'easy' or sys.argv[1] == 'hard', 'challenge mode must be "easy" or "hard"'

context.binary = elf = ELF(f'/challenge/monstrous-mangler-{sys.argv[1]}')

io = elf.process()

if sys.argv[1] == 'easy':
    '''
    0. len(input) = 0x25
    1. reverse input
    2. swap(input[22], input[35])
    3. xor mangler with key 0x7997e425241f4a
    4. repeat step 1 again
    5. swap(input[2], input[32])
    6. swap(input[1], input[5])
    7. repeat step 1 again
    '''

    final_key = [0x0A, 0xFA, 0x87, 0x41, 0x2F, 0x7B, 0x21, 0x1A, 0xE5, 0x8B, 0x43, 0x40, 0x68, 0x3B, 0x08, 0xE6, 0x86, 0x47, 0x4C, 0x69, 0x25, 0x17, 0xE0, 0x81, 0x55, 0x41, 0x69, 0x3C, 0x1E, 0xFC, 0x81, 0x1D, 0x45, 0x68, 0x40, 0x4E, 0xEF]
    input = final_key[::-1]
    input[1], input[5] = input[5], input[1]
    input[2], input[32] = input[32], input[2]
    input = input[::-1]
    input = xor(input, 0x7997e425241f4a.to_bytes(7, byteorder='big'))
    input = bytearray(input)
    input[22], input[35] = input[35], input[22]
    input = bytes(input)
    input = input[::-1]
    assert len(input) == 0x25, 'length of key must be 0x25'
    io.sendline(input)
else:
    '''
    0. len(input) = 0x25
    1. reverse input twice, NOTE: this step can be ignored
    2. xor mangler with key 0x0f03d3a0c62caf
    3. swap(input[22], input[31])
    4. reverse input
    5. swap(input[22], input[34])
    6. xor mangler with key 0xf584f763a791
    '''
    final_key = [0x9D, 0xFF, 0x3B, 0x3D, 0x0C, 0xF4, 0x49, 0xF2, 0x8A, 0xA9, 0xE1, 0x3F, 0x31, 0x39, 0x3F, 0x06, 0x6D, 0xD3, 0x43, 0x56, 0x4D, 0x0A, 0x00, 0x50, 0xBE, 0x2A, 0x3B, 0xC7, 0xC8, 0xEB, 0x3C, 0xCE, 0x58, 0xA4, 0xCB, 0xE8, 0x9C]
    input = xor(final_key, 0xf584f763a791.to_bytes(6, byteorder='big'))
    input = bytearray(input)
    input[22], input[34] = input[34], input[22]
    input = input[::-1]
    input[22], input[31] = input[31], input[22]
    input = xor(input, 0x0f03d3a0c62caf.to_bytes(7, byteorder='big'))
    assert len(input) == 0x25, 'length of key must be 0x25'
    io.sendline(input)

io.interactive()
