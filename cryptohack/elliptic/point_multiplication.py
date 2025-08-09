"""
Double and Add algorithm for the scalar multiplication
1. set Q = P and R = O
2. loop while n > 0:
   if n % 2 == 1, set R = R + Q
   else set Q = 2Q, n = n // 2
3. return R
"""

def addition(P, Q, a, p) :
    if P == (0, 0):
        return Q
    if Q == (0, 0):
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return (0, 0)

    if P == Q:
        lamb = (3 * x1 ** 2 + a) * pow((2 * y1), -1, p)
    else:
        lamb = (y2 - y1) * pow((x2 - x1), -1, p)
    x3 = lamb ** 2 - x1 - x2
    y3 = lamb * (x1 - x3) - y1
    return (x3 % p, y3 % p)
  

def scalar_multiplication(P, n, a, p):
    Q = P
    R = (0, 0)

    while n > 0:
        if n % 2 == 1:
            R = addition(R, Q, a, p)
        Q = addition(Q, Q, a, p)
        n = n //2
    return R

if __name__ == '__main__':
    a = 497
    p = 9739

    P = (2339, 2213)
    Q = scalar_multiplication(P, 7863, a, p)

    print(Q)
