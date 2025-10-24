from pwn import *
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} challenge_mode")

assert sys.argv[1] == "easy" or sys.argv[1] == "hard", (
    'challenge mode must be "easy" or "hard"'
)

context.binary = elf = ELF(f"/challenge/master-the-yancode-{sys.argv[1]}", checksec=False)

io = elf.process()

if sys.argv[1] == "easy":
    """
    memcpy(buf[0x6f], 0x7c3ffaf33dc8)
    buf[0x6f] += 0x8a
    buf[0x70] += 0x7f
    buf[0x71] += 0x3f
    buf[0x72] += 0x7b
    buf[0x73] += 0xbe
    buf[0x74] += 0x1f
    """
    origin_key = [0x7c, 0x3f, 0xfa, 0xf3, 0x3d, 0xc8]
    add_key = [0x8a, 0x7f, 0x3f, 0x7b, 0xbe, 0x1f]
    payload = []
    for i in range(len(origin_key)):
        payload.append((origin_key[i] + add_key[i]) & 0xff)
    io.sendline(bytes(payload))
else:
    origin_key = [0x51, 0x27, 0x31, 0x72, 0x35, 0x8, 0xdf, 0xb0, 0xd]
    add_key = [0xc2, 0x7c, 0x9d, 0x3, 0xe4, 0xfa, 0x84, 0x38, 0xa5]
    payload = []
    for i in range(len(origin_key)):
        payload.append((origin_key[i] + add_key[i]) & 0xff)
    io.sendline(bytes(payload))

io.interactive()
