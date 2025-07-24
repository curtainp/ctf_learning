"""
https://en.wikipedia.org/wiki/Euclidean_algorithm
"""


def gcd(a, b):
    """
    this algorithm cover all relationship between a and b
    """
    while b != 0:
        t = b
        b = a % b
        a = t
    return a


def main():
    print(gcd(12, 8))
    print(gcd(66528, 52920))


if __name__ == "__main__":
    main()
