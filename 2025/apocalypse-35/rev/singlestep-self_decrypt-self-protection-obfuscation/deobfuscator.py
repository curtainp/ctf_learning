from pwn import *
from capstone import *
import sys
import ctypes

cs = Cs(CS_ARCH_X86, CS_MODE_64)

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def deobfuscate(code, text_offset, text_end, addr, modified):
    stop = False
    while not stop:
        _, sz, mnemonic, op_str = next(cs.disasm_lite(code[addr:], 0)) # disasm_lite has info what we need but more faster
        if mnemonic == 'ret':
            stop = True
        elif mnemonic == 'call':
            call_dst = addr + ctypes.c_int64(int(op_str, 16)).value # must convert to int64, avoid overflow
            if call_dst >= text_offset and call_dst <= text_end:
                deobfuscate(code, text_offset, text_end, call_dst, modified)
        elif mnemonic == 'xor':
            if '[rip + ' in op_str:
                rip_offset = int(op_str.split('[rip + ')[1].split(']')[0], 16)
                key = int(op_str.split(',')[1], 16)
                decrypt = b''
                target_addr = addr + sz + rip_offset
                if op_str.startswith('qword ptr '):
                    decrypt = xor(p64(key), code[target_addr: target_addr + 8])
                elif op_str.startswith('dword ptr '):
                    decrypt = xor(p32(key), code[target_addr: target_addr + 4])
                elif op_str.startswith('word ptr '):
                    decrypt = xor(p16(key), code[target_addr: target_addr + 2])
                elif op_str.startswith('byte ptr '):
                    decrypt = xor(p8(key), code[target_addr: target_addr + 1])
                assert(len(decrypt) in [1, 2, 4, 8])
                for i, b in enumerate(decrypt):
                    modified[target_addr + i] = b
                for i in range(addr, addr + sz):
                    modified[i] = 0x90
                # the recover code may also have xor, here we need this to identity the pattern
                if code[addr - 1] == 0x9c: # pushf
                    modified[addr - 1] = 0x90
                if code[addr + sz] == 0x9d: # popf
                    modified[addr + sz] = 0x90
            elif '[rip - ' in op_str:
                for i in range(addr, addr + sz):
                    modified[i] = 0x90
                if code[addr - 1] == 0x9c:
                    modified[addr - 1] = 0x90
                if code[addr + sz] == 0x9d:
                    modified[addr + sz] = 0x90
            code = bytes(modified)
        addr += sz

def main():
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} obfuscated_file main_offset(hex number)')
        exit(1)
    elf = ELF(sys.argv[1])
    # binary stripped, we can't find main symbol automatically
    main_offset = int(sys.argv[2], 16)
    text_offset = elf.get_section_by_name('.text').header.sh_offset
    text_end = text_offset + elf.get_section_by_name('.text').header.sh_size
    with open(elf.path, 'rb') as f:
        full = f.read()
    data = full[:text_end]
    modified = bytearray(data)
    deobfuscate(data, text_offset, text_end, main_offset, modified)
    with open(f'{elf.path}_deobfuscated', 'wb') as f:
        f.write(bytes(modified) + full[text_end:])
        
if __name__ == '__main__':
    main()
