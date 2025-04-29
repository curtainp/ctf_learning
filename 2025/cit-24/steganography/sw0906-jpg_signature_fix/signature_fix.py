#!/usr/bin/env python3

fname = './yoda'
fix_fname = './yoda_fix'

def signature_fix(fname, fix_fname):
    with open(fname, 'rb') as f:
        data = f.read()
        
    fix_chunk = bytearray()
    
    for i in range(0, len(data), 4):
        chunk = data[i:i+4]
        if len(chunk) == 4:
            fix_chunk.extend(reversed(chunk))
        else:
            fix_chunk.extend(chunk)
            
    with open(fix_fname, 'wb') as f:
        f.write(fix_chunk)
        

signature_fix(fname, fix_fname)
