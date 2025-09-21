import hmac, hashlib, base64

secret = b'3df35e5dd772dd98a6feb5475d0459f8e18e08a46f48ec68234173663fca377b'
sid = 'amwvsLiDgNHm2XXfoynBUNRA2iWoEH5E'

sig = hmac.new(secret, sid.encode(), hashlib.sha256).digest()
sig_b64 = base64.b64encode(sig).decode().rstrip('=')

cookie = f's:{sid}.{sig_b64}'
print(f'connect.sid={cookie}')
