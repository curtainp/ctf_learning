# Description

I hashed 3 more of my most secret passwords with SHA256. To make the passwords even more unbreakable, I mutated each one according to the following rules:

- Password 1: Append 3 characters at the end, in the following order: a special character, a number, and an uppercase letter
- Password 2: A typo was made when typing the password. Consider a typo to mean a single-character deletion from the password
- Password 3: Make the password leet (and since I'm nice, I'll tell you a hint: only vowels are leetified!)

5e09f66ae5c6b2f4038eba26dc8e22d8aeb54f624d1d3ed96551e900dac7cf0d fb58c041b0059e8424ff1f8d2771fca9ab0f5dcdd10c48e7a67a9467aa8ebfa8 4ac53d04443e6786752ac78e2dc86f60a629e4639edacc6a5937146f3eacc30f

use =rockyou.txt=

# Solution

## Password 1

I use `hashcat` hydra mode (which can use all combinations from a given wordlist and mask), refer to: [Mask Attack](https://hashcat.net/wiki/doku.php?id=mask_attack)

```bash
hashcat -m 1470 5e09f66ae5c6b2f4038eba26dc8e22d8aeb54f624d1d3ed96551e900dac7cf0d -a6 rockyou.txt ?s?d?u
```

```bash
5e09f66ae5c6b2f4038eba26dc8e22d8aeb54f624d1d3ed96551e900dac7cf0d:hyepsi^4B

Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 1400 (SHA2-256)
Hash.Target......: 5e09f66ae5c6b2f4038eba26dc8e22d8aeb54f624d1d3ed9655...c7cf0d
Time.Started.....: Sat Jul 12 22:54:20 2025 (2 mins, 28 secs)
Time.Estimated...: Sat Jul 12 22:56:48 2025 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (rockyou.txt), Left Side
Guess.Mod........: Mask (?s?d?u) [3], Right Side
Guess.Queue.Base.: 1/1 (100.00%)
Guess.Queue.Mod..: 1/1 (100.00%)
Speed.#1.........:   425.5 MH/s (16.46ms) @ Accel:128 Loops:128 Thr:32 Vec:1
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 64115638272/123074814720 (52.09%)
Rejected.........: 0/64115638272 (0.00%)
Restore.Point....: 7454720/14344384 (51.97%)
Restore.Sub.#1...: Salt:0 Amplifier:2560-2688 Iteration:0-128
Candidate.Engine.: Device Generator
Candidates.#1....: idontgot1?7L -> hugnkiss09,6C
Hardware.Mon.SMC.: Fan0: 40%, Fan1: 39%
Hardware.Mon.#1..: Util: 98%
```

## Password 2

For this password, I ask _CHATGPT_ to write a script to generate the wordlist for me [wordlist_generate](./mutate_deletion.py), then straight use that for attack.

```bash

fb58c041b0059e8424ff1f8d2771fca9ab0f5dcdd10c48e7a67a9467aa8ebfa8:thecowsaysmo

Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 1400 (SHA2-256)
Hash.Target......: fb58c041b0059e8424ff1f8d2771fca9ab0f5dcdd10c48e7a67...8ebfa8
Time.Started.....: Sat Jul 12 23:10:55 2025 (0 secs)
Time.Estimated...: Sat Jul 12 23:10:55 2025 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (rockyou_deletion.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........: 27702.4 kH/s (9.39ms) @ Accel:1024 Loops:1 Thr:64 Vec:1
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 10092544/125488103 (8.04%)
Rejected.........: 0/10092544 (0.00%)
Restore.Point....: 9175040/125488103 (7.31%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: ooter! -> sasoun
Hardware.Mon.SMC.: Fan0: 40%, Fan1: 40%
Hardware.Mon.#1..: Util: 61%
```

## Password 3

The [crackstation](https://crackstation.net/) can crack this immediately.

```bash
unf0rg1v@bl3
```

> TIPS: after the ctf finished, I notice that `hashcat` has a builtin rule for [leetspeak](https://github.com/hashcat/hashcat/blob/master/rules/leetspeak.rule).
