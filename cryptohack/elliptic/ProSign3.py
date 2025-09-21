#!/usr/bin/env python

import hashlib
from Crypto.Util.number import bytes_to_long
from ecdsa.ecdsa import Public_key, Private_key, Signature, generator_192
from utils import listener
from datetime import datetime
from random import randrange

FLAG = "crypto{xxxxxxxxxxxxxxxxxx}"
g = generator_192
n = g.order()

class Challenge():
    def __init__(self):
        self.before_input = "Welcome to ProSign 3. You can sign time or verify.\n"
        secret = randrange(1, n)
        self.pubkey = Public_key(g, g * secret)
        self.privkey = Private_key(self.pubkey, secret)

    def sha1(self, data):
        sha1_hash = hashlib.sha1()
        sha1_hash.update(data)
        return sha1_hash.digest()

    def sign_time(self):
        now = datetime.now()
        m, n = int(now.strftime("%m")), int(now.strftime("%S"))
        current = f"{m}:{n}"
        msg = f"Current time is {current}"
        hsh = self.sha1(msg.encode())
        sig = self.privkey.sign(bytes_to_long(hsh), randrange(1, n))
        return {"msg": msg, "r": hex(sig.r), "s": hex(sig.s)}

    def verify(self, msg, sig_r, sig_s):
        hsh = bytes_to_long(self.sha1(msg.encode()))
        sig_r = int(sig_r, 16)
        sig_s = int(sig_s, 16)
        sig = Signature(sig_r, sig_s)

        if self.pubkey.verify(hsh, sig):
            return True
        else:
            return False

    # this challenge function is called on your input, which must be JSON encoded
    def challenge(self, input):
        if 'option' not in input:
            return {"error": "You must send an option to this server"}
        elif input["option"] == 'sign_time':
            signature = self.sign_time()
            return signature
        elif input["option"] == 'verify':
            msg = input['msg']
            r = input['r']
            s = input['s']
            verified = self.verify(msg, r, s)
            if verified:
                if msg == 'unlock':
                    self.exit = True
                    return {"FLAG": FLAG}
            else:
                return {'return': 'bad signature'}
        else:
            return {'error': 'decoding fail'}
        
import builtins; builtins.Challenge = Challenge
listener.start_server(port=13381)
