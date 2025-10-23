from pwn import *
import sys

if len(sys.argv) != 2:
    print(f'[x] Usages: {sys.argv[0]} [challenge_mode]')
    print(f'\t[example]{sys.argv[0]} easy\t\t\t will trigger easy mode challenge exp.')
    exit(1)

assert sys.argv[1] == 'easy' or sys.argv[1] == 'hard', 'challenge mode must be "easy" or "hard"'

context.binary = elf = ELF(f'/challenge/puzzle-patch-{sys.argv[1]}')

io = elf.process()

if sys.argv[1] == 'easy':
    '''
        call    _memcmp
        test    eax, eax
        jnz     short loc_1941

    this time only allow one byte patch, so we can:
    1. patch test eax, eax (85 C0) to xor eax, eax (31 C0)
    2. patch memcmp(src, dst, count) comparison size to 0, that always return equal!
    '''
    io.sendline(b'208c')        # offset of test eax, eax
    io.sendline(b'31')
    io.sendline(b'aaaaa')       # anything is ok
else:
    io.sendline(b'2009')        # offset of count
    io.sendline(b'0')
    io.sendline(b'aaaaa')

io.interactive()
