"""
the CRT gives a unique solution to a set of linear congruences if their moduli are coprime
"""

from functools import reduce

moduli = [5, 11, 17]
remainder = [2, 3, 5]

N = reduce(lambda x, y: x * y, moduli)

m = [N // m for m in moduli]
# when exponent is negative, this function use extend Euclidean algorithm to find the inverse modular
mi = [pow(m[i], -1, moduli[i]) for i in range(len(moduli))]

x = sum(a * mi[i] * m[i] for i, a in enumerate(remainder))

print(f"solution: {x % N}")
