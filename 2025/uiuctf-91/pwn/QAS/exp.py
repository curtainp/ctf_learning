from pwn import *

elf = context.binary = ELF("./dist/chal", checksec=False)

from z3 import *

s = Solver()

entropy = [0x91, 0x0B, 0xD7, 0x3D, 0x68, 0xC2, 0x95, 0x2B]
step1 = (entropy[0] << 8) | entropy[1]
step2 = (entropy[2] << 4) | (entropy[3] >> 4)
step3 = (entropy[4] * entropy[5]) & 0xFF
step4 = entropy[6] ^ entropy[7]
print(hex(step1), hex(step2), hex(step3), hex(step4))

input = BitVec("input", 16)
padding = BitVec("padding", 16)
input_ext = ZeroExt(16, input)
padding_ext = ZeroExt(16, padding)

s.add(((((input_ext ^ step1 ^ step2) + step3) ^ step4) | 0xEEE) ^ padding_ext == 0x555)

if s.check() == sat:
    input = s.model()[input]
    padding = s.model()[padding]
    print(input, padding)
else:
    print("not work")
