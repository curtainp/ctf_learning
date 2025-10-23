from pwn import *
import sys

if len(sys.argv) != 2:
    print(f'[x] Usages: {sys.argv[0]} [challenge_mode]')
    print(f'\t[example]{sys.argv[0]} easy\t\t\t will trigger easy mode challenge exp.')
    exit(1)

assert sys.argv[1] == 'easy' or sys.argv[1] == 'hard', 'challenge mode must be "easy" or "hard"'

context.binary = elf = ELF(f'/challenge/patched-up-{sys.argv[1]}')

io = elf.process()

if sys.argv[1] == 'easy':
    '''
        call    _memcmp
        test    eax, eax
        jnz     short loc_1941

    nop out the jnz instruction
    '''
    io.sendline(b'192b')
    io.sendline(b'90')
    io.sendline(b'192c')
    io.sendline(b'90')
    for _ in range(6):
        io.sendline(b'0')
    io.sendline(b'aaaaa')       # anything is ok
else:
    io.sendline(b'226b')
    io.sendline(b'90')
    io.sendline(b'226c')
    io.sendline(b'90')
    for _ in range(6):
        io.sendline(b'0')
    io.sendline(b'aaaaa')

io.interactive()
