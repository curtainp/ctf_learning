#!/usr/bin/env python3

def decrypt_input(final_key):
    """
    Reverse the encryption operation:
    final_key[i] = ((input[i] + 123) >> 4) | (16 * (input[i] + 123))
    
    To decrypt:
    1. Let temp = input[i] + 123
    2. final_key[i] = (temp >> 4) | (16 * temp)
    3. final_key[i] = (temp >> 4) | (temp << 4)
    4. This swaps the nibbles of temp (low 4 bits become high, high 4 bits become low)
    5. To reverse: swap nibbles back, then subtract 123
    """
    input_array = []
    
    for encrypted_byte in final_key:
        # Convert to byte value if it's a character
        if isinstance(encrypted_byte, str):
            encrypted_byte = ord(encrypted_byte)
        
        # Reverse the nibble swap: swap high and low 4 bits back
        # encrypted_byte has nibbles swapped, so swap them back
        temp = ((encrypted_byte & 0x0F) << 4) | ((encrypted_byte & 0xF0) >> 4)
        
        # Subtract 123 to get original input
        original = (temp - 123) & 0xFF  # Keep it as a byte
        input_array.append(original)
    
    return input_array


def main():
    # Given final key
    final_key = 'VLFDYyhuaVqbRBTY'
    
    print(f"Encrypted key: {final_key}")
    print(f"Encrypted key (hex): {final_key.encode().hex()}")
    print()
    
    # Decrypt
    decrypted = decrypt_input(final_key)
    
    print("Decrypted input array:")
    print(f"Decimal: {decrypted}")
    print(f"Hex: {[hex(x) for x in decrypted]}")
    print(f"bytes: {bytes(decrypted)}")
    print(f"ASCII (if printable): {''.join(chr(x) if 32 <= x < 127 else '.' for x in decrypted)}")
    
    # Verify encryption
    print("\n--- Verification ---")
    print("Re-encrypting to verify:")
    verified = []
    for val in decrypted:
        temp = (val + 123) & 0xFF
        encrypted = ((temp >> 4) | (16 * temp)) & 0xFF
        verified.append(chr(encrypted))
    
    verified_str = ''.join(verified)
    print(f"Re-encrypted: {verified_str}")
    print(f"Matches original: {verified_str == final_key}")


if __name__ == "__main__":
    main()
