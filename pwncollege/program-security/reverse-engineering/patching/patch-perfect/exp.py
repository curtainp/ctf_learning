from pwn import *
import sys

if len(sys.argv) != 2:
    print(f'[x] Usages: {sys.argv[0]} [challenge_mode]')
    print(f'\t[example]{sys.argv[0]} easy\t\t\t will trigger easy mode challenge exp.')
    exit(1)

assert sys.argv[1] == 'easy' or sys.argv[1] == 'hard', 'challenge mode must be "easy" or "hard"'

context.binary = elf = ELF(f'/challenge/patch-perfect-{sys.argv[1]}')

io = elf.process()

if sys.argv[1] == 'easy':
    '''
    this challenge will perform integrity check. and we only have 2 byte patch.
    so we patch each count of memcmp
    '''
    io.sendline(b'1d97')        # offset of first memcmp count (integrity check)
    io.sendline(b'0')
    io.sendline(b'202a')        # offset of second memcmp count (input key check)
    io.sendline(b'0')
    io.sendline(b'aaaaa')       # anything is ok
else:
    io.sendline(b'1f80')
    io.sendline(b'0')
    io.sendline(b'205b')
    io.sendline(b'0')
    io.sendline(b'aaaaa')

io.interactive()
