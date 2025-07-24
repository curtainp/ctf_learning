exec(open("./modular_binomials.txt", "r").read())

# """
# ```latex
# $N = p*q$
# $c1 = (2p+3q)^{e1} mod N$
# $c_2 = (5p + 7q)^{e_2} mod N$

# $c_1^{e_2} = (2p + 3q)^{(e_1e_2)}\ mod\ N$
# $c_2^{e_1} = (5p + 7q)^{(e_1e_2)}\ mod\ N$

# $f_1 = 5^{e_1e_2} * c_1^{e_2} = (10p + 15q)^{(e_1e_2)}\ mod \ N$
# $f_2 = 2^{e_1e_2} * c_2^{e_1} = (10p + 14q)^ {(e_1e_2)}\ mod \ N$

# $f_1-f_2=q^{(e_1*e_2)}\ mod\ N$
# $q = gcd((f_1-f_2),N)$
# ```
# """

from math import gcd

q = gcd(
    (pow(5, e1 * e2, N) * pow(c1, e2, N)) - (pow(2, e1 * e2, N) * pow(c2, e1, N)), N
)
p = N // int(q)

print(f"crypto{{{p},{q}}}")
