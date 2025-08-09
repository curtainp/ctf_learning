"""
for F(9739): Y2 = X3 + 497X + 1768
that with P(8045, 6936), compute which point Q satisfied that:
P + Q = O, in which case O is infinity point.

Solution:

according to the description above, Q = -P, which is symmetry around the axis x

case that Curve defined in Finite Field don't allow negative number, which should modular p
"""
p = 9739

P = (8045, 6936)
Q = [P[0], -P[1]]
Q[1] %= p

print(Q)
