"""
AES_CBC decrypt:
P_i = Ci ^ C_(i-1) while C_0 = iv

this email service reuse the cipher suite to encrypto/decrypto the valiation from user.

we can leverage first encrypto result to construction the second, according the decrypto procedure.

what we need:
xxx,email,xxx@script.sorcerer    => here   ,email,x is 32bytes occupy 2 block and tail occupy 1 block

we split (,email,x) to separate block, first_part = first_part ^ 0 = first_part ^ (C_i ^ C_(i-1) ^ P_i)

(C_i C_(i-1) P_i) all known before encryption
"""
from pwn import *

host = 'play.scriptsorcerers.xyz'
port = 10417

def main():
    io = remote(host, port)

    _ = io.recvuntil(b'Your Email is: ')
    email = io.recvline().strip()
    print(f'[+] Email: {email.decode()} Len: {len(email)}')

    """
    build password need satisfied following condition:
    1. len(password) % 16 == 0
    2. b"@script.sorcerer" with len equal to 16 not in password
    3. email not in password
    """
    target32 = b',' + email + b',' + b'x' * (32 - (len(email) + 2))
    target_first_half = target32[:16]
    target_last_half = target32[16:32]

    P1 = b'A' * 16
    P2 = b'B' * 16
    P4 = b'C' * 16
    P5 = b'D' * 16

    password = P1 + P2 + target_last_half + P4 + P5

    _ = io.recvuntil(b"Please use this key for future login: ")
    enc = bytes.fromhex(io.recvline().strip().decode())
    C = [enc[i:i+16] for i in range(0, len(enc), 16)]
    C1, C2, C3, C4, C5 = C      # this must be 5 block, cause input is 5 block
    """
    Here:
    C1 = P1 ^ iv
    C2 = P2 ^ C1
    C3 = target_last_half ^ C2
    C4 = P4 ^ C3
    C5 = P5 ^ C4

    """

    tail_block = b'@script.sorcerer'
    C11 = xor(xor(C1, P2), target_first_half)
    # when decrypt, P22 = C2 ^ C11 = C2 ^ (C1 ^ P2) ^ target_first_half = target_first_half
    C22 = C2
    C33 = C3
    C44 = xor(xor(C4, P5), tail_block)
    C55 = C5

    final = C11 + C22 + C33 + C44 + C55

    _ = io.sendlineafter(b'Enter your choice: ', b'2')
    _ = io.sendlineafter(b'(in hex): ', final.hex().encode())

    _ = io.sendlineafter(b'Enter your choice: ', b'1')

    print(io.recvall())


if __name__ == '__main__':
    main()


