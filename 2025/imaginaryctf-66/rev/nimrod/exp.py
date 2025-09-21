from pwn import xor

enc = bytes.fromhex('28F83EE63E2F430CB996D15CD6BF36D820790E8E5221B250E398B5C9B8A08830D90A')

key = 0x13371337

key_final = b''
for _ in range(len(enc)):
    key = (((key * 0x19660d) & 0xffffffff) + 0x3C6EF35F) & 0xffffffff
    key_final += ((key >> 0x10) & 0xff).to_bytes()

print(xor(key_final, enc).decode())
