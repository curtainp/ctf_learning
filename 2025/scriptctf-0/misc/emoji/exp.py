import codecs

with codecs.open('./out.txt', encoding='utf-8') as f:
    data = f.read()

flag = ''
for d in data:
    flag += chr(ord(d) & 0xff)

print(flag)
