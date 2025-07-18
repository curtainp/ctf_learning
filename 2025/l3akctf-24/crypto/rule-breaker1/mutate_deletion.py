import sys

for line in sys.stdin.buffer:
    try:
        word = line.decode('utf-8', errors='ignore').strip()
        for i in range(len(word)):
            print(word[:i] + word[i + 1:])
    except UnicodeDecodeError:
        continue
