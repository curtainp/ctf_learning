import re, zlib

with open('./challenge.pdf', 'rb') as f:
    data = f.read()

# get all stream objects
streams = re.findall(br"stream[\r\n]+(.*?)endstream", data, re.DOTALL)

for i, obj in enumerate(streams):
    print(f"[+] Stream {i} --- length {len(obj)} bytes")
    try:
        decode_data = zlib.decompress(obj).decode('utf-8', errors='ignore')
        print(f"[+] Decompress text: {decode_data}")
    except Exception as e:
        print(f"[!] Couldn't decompress, just ignore it")

