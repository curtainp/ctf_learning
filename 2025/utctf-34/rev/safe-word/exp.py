'''
from disassembler result, we can get that:
    this program need us input the correct flag, use that flag one by one to step forward
    the "logic table in memory", which initial use the hardcode.
'''

from capstone import *

dis = Cs(CS_ARCH_X86, CS_MODE_64)

chal = open('./chal', 'rb').read()

flag = 'utflag{1_w4nna_pl4y_hypix3l_in_c}'
init = [0x2d800]

indexs = []

def check_inst(inst: bytes):
    # print(inst.hex(), end= ' ')
    mnemonics = []
    ops = []
    for (_, _, nes, op_str) in dis.disasm_lite(inst, 0x0):
        ops.append(op_str)
        mnemonics.append(nes)
    # print(mnemonics, end=' ')
    # print(ops)
    if len(mnemonics) == 3 and  mnemonics[0] == 'push' and mnemonics[1] == 'pop' and mnemonics[2] == 'ret':
        # print('check inst: ', inst.hex())
        print(hex(indexs[-1]), end=' ')
        print(inst.hex(), end=' ')
        print(mnemonics, ops, end=' ')
        if len(ops) != 0 and '0x' in ops[0]:
            a = (int(ops[0].split('0x')[1], 16) << 8) * 8
        else:
            a = (int(ops[0], 16) << 8) * 8
        print(hex(a))
        start = hex(a)[2:]
        init.append(a)
        return True
    else:
        return False


start = 0x12d2
# start = 0xb05c
end = 0x13389
for (_, _, mnemonic, op_str) in dis.disasm_lite(chal[start:end], 0x0):
    if mnemonic == 'add' and '0x' in op_str:
        index = int(op_str.split('0x')[1], 16)
        indexs.append(index)
        # print(hex(index))
    if mnemonic == 'mov' and '0x' in op_str:
        a = op_str.split('0x')[1].rjust(8, '0')
        # print(a)
        b = bytes.fromhex(a)
        c = int.from_bytes(b, 'little')
        d = hex(c)[2:].rjust(8, '0')
        e = bytes.fromhex(d)
        # print(inst.hex())
        if not check_inst(e):
            indexs.pop()
        # else:
        #     a = init[-1]
        #     start = 


print(' '.join(hex(x) for x in init))
print(' '.join(hex(x) for x in indexs))

# print(len(init), len(indexs))

# for a, b in zip(init, indexs):
#     print(hex(b), hex(a))
#     c = (b - a) // 8
#     flag += chr(c)
# print(flag)
