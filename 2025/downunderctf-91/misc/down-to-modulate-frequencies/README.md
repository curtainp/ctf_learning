# Solution

refer to: https://www.dcode.fr/dtmf-code

but the data seems like the sum of the frequencies.

```python
DTMF_KEYS = {
    (697, 1209): '1',
    (697, 1336): '2',
    (697, 1477): '3',
    (697, 1633): 'A',
    (770, 1209): '4',
    (770, 1336): '5',
    (770, 1477): '6',
    (770, 1633): 'B',
    (852, 1209): '7',
    (852, 1336): '8',
    (852, 1477): '9',
    (852, 1633): 'C',
    (941, 1209): '*',
    (941, 1336): '0',
    (941, 1477): '#',
    (941, 1633): 'D',
}

sum_to_key = {low + high: key for (low, high), key in DTMF_KEYS.items()}

data = open('./dist/dtmf.txt', 'r').read()

chunks = [int(data[i: i + 4]) for i in range(0, len(data), 4)]

decode = ''
for c in chunks:
  decode += sum_to_key.get(c, '?')

print(f'decode from dtmf: {decode}')
```

after DTMF decode, the data seems still encoded with SMS [multiple-abc-cipher](https://www.dcode.fr/multitap-abc-cipher)

```python

T9_KEYS = {
    '1': ['.', ',', '?', '!', '1'],
    '2': ['A', 'B', 'C', '2'],
    '3': ['D', 'E', 'F', '3'],
    '4': ['G', 'H', 'I', '4'],
    '5': ['J', 'K', 'L', '5'],
    '6': ['M', 'N', 'O', '6'],
    '7': ['P', 'Q', 'R', 'S', '7'],
    '8': ['T', 'U', 'V', '8'],
    '9': ['W', 'X', 'Y', 'Z', '9'],
    '0': [' '],  # Typically 0 is space in T9
    '#': ['']
}

import itertools

t9_decode = ''
for key, group in itertools.groupby(decode):
  presses = len(list(group))
  if key in T9_KEYS:
    chars = T9_KEYS[key]
    index = (presses - 1) % len(chars)
    t9_decode += chars[index]
  else:
    t9_decode += key

print(f'final decode: {t9_decode}')
```
