test_pt = [
    0x2265B1F5,
    0x91B7584A,
    0xD8F16ADF,
    0xCD613E30,
    0xC386BBC4,
    0x1027C4D1,
    0x414C343C,
    0x1E2FEB89,
]
test_ct = [
    0xDC44BF5E,
    0x5AFF1CEC,
    0xE1E9B4C2,
    0x01329B92,
    0x8F9CA92A,
    0x0E45C5B4,
    0x604A4B91,
    0x7081EB59,
]
flag_enc = [
    0x24189111,
    0xFD94E945,
    0x1B9F64A6,
    0x7FECE9A3,
    0xFC2A0EDE,
    0x576EDCF5,
    0x01E44C9C,
    0x658AF790,
]

KEY = 0xFFFFFF2F


from z3 import *


def z3_method():
    s = Solver()

    input = [BitVec(f"input_{i}", 32) for i in range(len(flag_enc))]

    # Actually, this is a discrete logarithm
    def F(a1, a2, a3):
        v5 = 1
        v6 = a1 % a3
        while a2 > 0:
            if (a2 & 1) != 0:
                v5 = v6 * v5 % a3
            v6 = v6 * v6 % a3
            a2 >>= 1
        return v5

    def F_z3(a1, a2, a3):
        v5 = 1
        v6 = a1 % a3
        for i in range(32):
            bit_i = Extract(i, i, a2)
            v5 = If(bit_i == 1, v6 * v5 % a3, v5)
            v6 = v6 * v6 % a3
        return v5

    for i in range(len(flag_enc)):
        s.add(F_z3(test_pt[i], input[i], KEY) == test_ct[i])

    if s.check() == sat:
        print(s.model())
    else:
        print("not work")


from sympy.ntheory import discrete_log

input_value = []
for i in range(8):
    base = test_pt[i]
    target = test_ct[i]
    try:
        x = discrete_log(KEY, target, base)
        input_value.append(x % KEY)
    except ValueError:
        print(f"No discrete log found for i={i}")
        input_value.append(0)

print(f"input: {input_value}")
