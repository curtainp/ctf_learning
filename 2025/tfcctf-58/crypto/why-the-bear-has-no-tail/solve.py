#!/usr/bin/env python3
from pwn import remote
import re
import ast, re
from cracker import Untwister

MENU_PROMPT = b"Enter your choice: "
ROUND_START = b"what you finna do, huh?"
END_OF_BUFFER = b"Reached end of buffer"
HOST = "the-bear-4781ecf58b6255f9.challs.tfcctf.com"
PORT = 1337

SAMPLE_RE = re.compile(rb"idk what u finna do with it:\s*(\d+)")

def parse_sample(blob: bytes):
    if END_OF_BUFFER in blob:
        return None
    m = SAMPLE_RE.search(blob)
    if m:
        return int(m.group(1))
    ints = re.findall(rb"(\d+)", blob)
    if ints:
        return int(ints[-1])
    return None

def recover_flag(samples, encrypted_flag):
    ut = Untwister()

    # Submit each 32-bit tempered output with unknown high 6 bits.
    # Submit full 32-bit unknown
    for sample in samples:
        bits = f"{sample:026b}".replace("0b", "") + "?" * 6
        assert len(bits) == 32
        ut.submit(bits)
        ut.submit("?" * 32)

    r2 = ut.get_random()
    L = len(encrypted_flag)

    idxs = [i for i in range(256)]
    key = r2.choices(idxs, k=L)
    flag = "".join(chr(e ^ k) for e, k in zip(encrypted_flag, key))
    return flag

def solve():
    r = remote(HOST, PORT, ssl=True)
    samples = []
    try:
        r.recvuntil(MENU_PROMPT)
        for _ in range(1400):
            r.sendline(b"1")
            blob = r.recvuntil(ROUND_START)

            sample = parse_sample(blob)
            samples.append(sample)
            r.recvuntil(MENU_PROMPT)

        print(f"Collected {len(samples)} samples")
        r.sendline(b"2")
        blob = r.recvuntil(ROUND_START)

        # Extract the printed list from the blob
        m = re.search(rb"\[.*\]", blob, re.S)
        if not m:
            print("No omlet found")
            return
        omlet = ast.literal_eval(m.group().decode())
        print(omlet)
        print("Recovered flag: ", recover_flag(samples, omlet))
        r.recvuntil(MENU_PROMPT)
    finally:
        r.close()

if __name__ == "__main__":
    # Connect with TLS
    solve()
