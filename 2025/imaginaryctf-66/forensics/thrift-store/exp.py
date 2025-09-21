from pwn import *

CONSTANTS = {
    "stop": b"\x00",
    "binary_protocol": b"\x80",
    "version": b"\x00\x01",
    "type_call": b"\x01",
}

io = remote("thrift-store.chal.imaginaryctf.org", "9000")
