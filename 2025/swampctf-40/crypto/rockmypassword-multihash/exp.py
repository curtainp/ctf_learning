#!/usr/bin/env python

import hashlib


def multi_hash(text):
    flag = text.encode()
    for _ in range(100):
        flag = hashlib.md5(flag).digest()

    for _ in range(100):
        flag = hashlib.sha256(flag).digest()

    for _ in range(100):
        flag = hashlib.sha512(flag).digest()
    return flag.hex()

target_hash = "f600d59a5cdd245a45297079299f2fcd811a8c5461d979f09b73d21b11fbb4f899389e588745c6a9af13749eebbdc2e72336cc57ccf90953e6f9096996a58dcc"

def main():
    with open('./rockyou-10.txt', 'r', encoding='latin-1') as f:
        for password in f:
            password = password.strip()
            if len(password) != 10:
                continue
            flag = "swampCTF{" + password + "}"
            flag_hash = multi_hash(flag)
            if flag_hash == target_hash:
                print(f"Found password: {flag}")
                break

if __name__ == '__main__':
    main()
