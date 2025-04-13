# solution

login with password we get a **only root group can read** flag.txt, so we need privilege
escalation.

Is the `flag.txt` can only be read by root group?
no, there another file permission exist in Linux.
`getfacl setfacl`. by this, we can get that `secretuser` can read flag.

## list user of system

`cat /etc/passwd`, we get hint that there is a `secretuser` within system. and most important
there is a comment with the `password` that user.

## change to secretuser

we use that password login `secretuser`, and read the flag.
