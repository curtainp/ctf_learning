"""
Four properties of XOR operations:
1. commutative: A ^ B = B ^ A
2. associative: A ^ (B ^ C) = (A ^ B) ^ C
3. identity: A ^ 0 = A
4. self-inverse: A ^ A = 0
"""

KEY1 = 0xA6C8B6733C9B22DE7BC0253266A3867DF55ACDE8635E19C73313
KEY2_KEY1 = 0x37DCB292030FAA90D07EEC17E3B1C6D8DAF94C35D4C9191A5E1E
KEY2_KEY3 = 0xC1545756687E7573DB23AA1C3452A098B71A7FBF0FDDDDDE5FC1
FLAG_KEY1_KEY3_KEY2 = 0x04EE9855208A2CD59091D04767AE47963170D1660DF7F56F5FAF

flag = hex(FLAG_KEY1_KEY3_KEY2 ^ KEY1 ^ KEY2_KEY3)

print(bytes.fromhex(flag[2:]))

# NOTE: the other way to solve this is use
# from pwn import xor
# which can xor between bytes, normally this operation is not allow.
