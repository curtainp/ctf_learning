MASK = (1 << 64) - 1
KEYS = [0x00001337DEADBEEF, 0x0000C0DE12345678, 0x0000ABCDEF012345, 0x00009876543210AB]
EXPECTED = [
    0xFD83487A8F04BC91,
    0x1EA9B29316416331,
    0x2FBEA4546B08944F,
    0x922E9E7E9854DCAF,
]


def rol(value, shift, bits=64):
    shift %= bits
    return ((value << shift) | (value >> (bits - shift))) & MASK


def sub_4011f6(value, key):
    xor_value = value ^ key

    return ((xor_value * 0x1F) & MASK) ^ rol(xor_value, 0xD)


def sub_401234(value1, value2):
    for i in range(4):
        value2_1 = value2
        value2 = value1 ^ sub_4011f6(value2, KEYS[i])
        value1 = value2_1

    return value1, value2


def reverse_sub_401234(value1, value2):
    for i in reversed(range(4)):
        value1_1 = value1
        value1 = value2 ^ sub_4011f6(value1, KEYS[i])
        value2 = value1_1

    return value1, value2


def int2bytes(num):
    return num.to_bytes(8, "little")


def main():
    res = b""
    for i in range(0, len(EXPECTED), 2):
        part1, part2 = reverse_sub_401234(EXPECTED[i], EXPECTED[i + 1])

        res += int2bytes(part1)
        res += int2bytes(part2)

    print(res)


if __name__ == "__main__":
    main()
