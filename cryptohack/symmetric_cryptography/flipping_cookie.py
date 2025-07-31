"""
this challenge give us a iv and ciphertext with CBC mode of AES encrypto, the ciphertext is encrypted with cookie, which has user info.
we need to forge this user info to `admin=True`


"""
import requests
from Crypto.Util.strxor import strxor

def get_cookie():
    r = requests.get('http://aes.cryptohack.org/flipping_cookie/get_cookie/')
    return r.json()['cookie']

def check_admin(cookie, iv):
    r = requests.get(f'http://aes.cryptohack.org/flipping_cookie/check_admin/{cookie}/{iv}/')
    return r.json()['flag']

cookie = get_cookie()
iv = bytes.fromhex(cookie[:32])

# this plaintext length is 16, for first block, we will forge a fake iv = text ^ origin_iv ^ forge_text
# when call check_admin, the decrypt procedure the first block ^ fake_iv will eliminate text, cause they are identity
text = b'admin=False;expi'
forge_text = b'admin=True;expir'

forge_iv = strxor(strxor(text, iv), forge_text).hex()

assert len(forge_iv) == 32, 'failed to constructure fake iv'

print(check_admin(cookie[32:], forge_iv))
