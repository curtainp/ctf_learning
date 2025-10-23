from pwn import *
import sys

if len(sys.argv) != 2:
    print(f'[x] Usages: {sys.argv[0]} [challenge_mode]')
    print(f'\t[example]{sys.argv[0]} easy\t\t\t will trigger easy mode challenge exp.')
    exit(1)

assert sys.argv[1] == 'easy' or sys.argv[1] == 'hard', 'challenge mode must be "easy" or "hard"'

context.binary = elf = ELF(f'/challenge/tangled-ticket-{sys.argv[1]}')

io = elf.process()

# swap(key[2], key[4])
if sys.argv[1] == 'easy':
    io.sendline(b'mdqkt')
else:
    io.sendline(b'zapim')

io.interactive()
