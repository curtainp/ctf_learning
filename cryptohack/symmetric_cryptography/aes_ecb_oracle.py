from Crypto.Cipher import AES
import string
import time
import requests

def encrypt(payload: str) -> str:
    url = 'http://aes.cryptohack.org/ecb_oracle/encrypt/'
    r = requests.get(url + payload + '/')
    return r.json()['ciphertext']

def print_blk(hex_blk: str, sz: int):
    for i in range(0, len(hex_blk), sz):
        print(hex_blk[i: i+sz], ' ', end='')
    print()
    
def bruteforce():
    flag = ''
    # after some investigation, we can notice that when probe size equal to 7, the result one block length added compare to before(32)
    # So the flag length = 32 - 7 = 25, here we have to use second block for probe.
    probe_block_sz = 32 - 1
    alphabet = '{' + '_' + '@' + '}' + string.digits + string.ascii_lowercase + string.ascii_uppercase
    
    while True:
        payload = '1' * (probe_block_sz - len(flag))
        expected = encrypt(payload.encode().hex())
        print('Expected:', end=' ')
        print_blk(expected, 32)
        
        for c in alphabet:
            res = encrypt(bytes.hex((payload + flag + c).encode()))
            
            if res[32:64] == expected[32:64]:
                flag += c
                print(c, ':', end='')
                print_blk(res, 32)
                break
            time.sleep(1)
            
        if flag.endswith('}'):
            break
    print(flag)
    
if __name__ == '__main__':
    bruteforce()
            
            
