import capstone, capstone.x86 as x86
from pwn import *

with open('./chal', 'rb') as f:
    data = f.read()

cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
cs.detail = True

solution = []
seen = set()

def try_per_ascii(i, j):
    addr = ((i << 8) + j) * 8
    insns = list(cs.disasm(data[addr: addr+8], 0))
    if not any(x.id == x86.X86_INS_RET for x in insns):
        return -1
    if len(insns) < 3:
        return -1
    if [x.id for x in insns[:3]] == [x86.X86_INS_PUSH, x86.X86_INS_POP, x86.X86_INS_RET]:
        jj = insns[0].operands[0].imm
        if jj not in seen:
            print(f"--- tbl {i} / char {j} {chr(j)}")
            for x in insns[:3]:
                print(f"0x{x.address:04x}: {x.mnemonic:10s} {x.op_str:s}")
            return jj
    return -1


d = dict()
for i in range(0x80):
    for j in range(32, 128):
        k = try_per_ascii(i, j)
        if k >= 0:
            d.setdefault(i, []).append((k, chr(j)))


print(d)
print(len(d))
