from pwn import *
import sys

if len(sys.argv) != 2:
    print(f'[x] Usages: {sys.argv[0]} [challenge_mode]')
    print(f'\t[example]{sys.argv[0]} easy\t\t\t will trigger easy mode challenge exp.')
    exit(1)

assert sys.argv[1] == 'easy' or sys.argv[1] == 'hard', 'challenge mode must be "easy" or "hard"'

context.binary = elf = ELF(f'/challenge/trust-the-yancode-{sys.argv[1]}')

io = elf.process()

if sys.argv[1] == 'easy':
    '''
    emulator do something like this:
    read(0, buf[0x7f], 8)
    i = 0x9f
    buf[i++] = 0x4e
    buf[i++] = 0xe0
    buf[i++] = 0xaf
    buf[i++] = 0x3f
    buf[i++] = 0x94
    buf[i++] = 0xae
    buf[i++] = 0x4d
    buf[i++] = 0x62

    memcmp(buf[0x7f], buf[0x9f], 0)
    '''
    io.sendline(b'\x4e\xe0\xaf\x3f\x94\xae\x4d\x62')
else:
    io.sendline(b'\xf3\xa7\x8a\xdc\x6f\x95')

io.interactive()
