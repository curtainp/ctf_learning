def dword2b(d: int):
    return (d & 0xffffffff) & 0xff

def dword(d: int):
    return d & 0xffffffff

def off(d: int):
    return dword2b(d + 15)

def reverse_off(d: int):
    return dword2b(d - 15)

def eor(d: int):
    return dword2b(d ^ 0x69)

def rtr(d: int):
    return dword2b(dword(d >> 1) | dword(d << 7))

def reverse_rtr(d: int):
    return dword2b(dword(d << 1) | dword(d >> 7))

enc = bytes.fromhex('9407d46407546324ad98457235')

flag = 'ictf{'

flag += chr(reverse_off(eor(reverse_rtr(enc[0]))))
flag += chr(eor(enc[1]))
flag += chr(reverse_rtr(reverse_off(reverse_rtr(enc[2]))))
flag += chr(reverse_rtr(reverse_rtr(eor(enc[3]))))
flag += chr(eor(enc[4]))
flag += chr(reverse_rtr(reverse_off(reverse_rtr(enc[5]))))
flag += chr(reverse_rtr(eor(reverse_rtr(enc[6]))))
flag += chr(reverse_rtr(reverse_rtr(eor(enc[7]))))
flag += chr(reverse_rtr(reverse_off(eor(enc[8]))))
flag += chr(reverse_rtr(enc[9]))
flag += chr(reverse_off(reverse_off(reverse_rtr(enc[10]))))
flag += chr(reverse_rtr(reverse_rtr(eor(enc[11]))))
flag += chr(eor(reverse_off(reverse_rtr(enc[12]))))
flag += '}'
# flag += chr(reverse_off(eor(reverse_off(enc[13]))))

print(flag)

