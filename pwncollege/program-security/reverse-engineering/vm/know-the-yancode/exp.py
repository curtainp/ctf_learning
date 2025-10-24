from pwn import *
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} challenge_mode")

assert sys.argv[1] == "easy" or sys.argv[1] == "hard", (
    'challenge mode must be "easy" or "hard"'
)

context.binary = elf = ELF(f"/challenge/know-the-yancode-{sys.argv[1]}", checksec=False)

io = elf.process()

if sys.argv[1] == "easy":
    """
    1. call read(0, buf[68], 8)
    2. memcpy(buf[100], 0xbfcf7ee331eaa06a)
    3. memcmp(buf[68], buf[100])
    4. memcmp must return success
    """
    io.sendline(0x32E48EEED720CB69.to_bytes(8, byteorder="big"))
else:
    io.sendline(0xBFCF7EE331EAA06A.to_bytes(8, byteorder="big"))

io.interactive()
