from pwn import *
import sys

if len(sys.argv) != 2:
    print(f'[x] Usages: {sys.argv[0]} [challenge_mode]')
    print(f'\t[example]{sys.argv[0]} easy\t\t\t will trigger easy mode challenge exp.')
    exit(1)

assert sys.argv[1] == 'easy' or sys.argv[1] == 'hard', 'challenge mode must be "easy" or "hard"'

context.binary = elf = ELF(f'/challenge/meager-mangler-{sys.argv[1]}')

io = elf.process()

if sys.argv[1] == 'easy':
    '''
    0. len(input) = 18
    1. xor mangler with key 0xc753fb
    2. swap(input[15], input[16])
    3. xor mangler with key 0xde48
    '''
    final_key = [0x71, 0x73, 0x4B, 0xEB, 0xE5, 0xD8, 0x7F, 0x6C, 0x49, 0xED, 0xFA, 0xD6, 0x60, 0x77, 0x47, 0x72, 0x69, 0xC0]
    rev_stage3 = xor(bytes(final_key), 0xde48.to_bytes(2, byteorder='big'))
    rev_stage3 = bytearray(rev_stage3)
    rev_stage3[15], rev_stage3[16] = rev_stage3[16], rev_stage3[15]
    rev_stage3 = bytes(rev_stage3)
    rev_stage1 = xor(rev_stage3, 0xc753fb.to_bytes(3, byteorder='big'))

    assert len(rev_stage1) == 18, 'length of key must be 18'
    io.sendline(rev_stage1)
else:
    '''
    0. len(input) = 18
    1. swap each element from both ends to the middle
    2. swap(input[3], input[5])
    3. repeat step1 again
    '''
    final_key = b'ydzcxcpshmhqnonlcw'

    def swap_both_ends(input):
        for i in range(9):
            temp = input[i]
            input[i] = input[17 - i]
            input[17 - i] = temp
        return input
    rev_stage3 = swap_both_ends(list(final_key))
    rev_stage3[3], rev_stage3[5] = rev_stage3[5], rev_stage3[3]
    rev_stage1 = swap_both_ends(rev_stage3)

    assert len(rev_stage1) == 18, 'length of key must be 18'

    io.sendline(bytes(rev_stage1))

io.interactive()
