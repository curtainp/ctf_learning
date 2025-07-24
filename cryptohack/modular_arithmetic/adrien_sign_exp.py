exec("result_list =" + open("./adrien_output.txt", "r").read())

a = 288260533169915
p = 1007621497415251

# compute legendre symbol
a_p = pow(a, (p - 1) // 2, p)
print(a_p)
# this indicate that a is quadratic residue, so a ^ e also is. when plaintext_bit == 1, n is appended to ciphertext. so n is quadratic residue too. Or the plaintext_bit == 0

plain_text = ""

for r in result_list:
    N = pow(r, (p - 1) // 2, p)
    if N == 1:  # is quadratic residue
        plain_text += "1"
    else:
        plain_text += "0"


flag = ""
for i in range(0, len(plain_text), 8):
    flag += chr(int(plain_text[i : i + 8], 2))
print(flag)
