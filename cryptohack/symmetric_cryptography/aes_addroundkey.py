state = [
    [206, 243, 61, 34],
    [171, 11, 93, 31],
    [16, 200, 91, 108],
    [150, 3, 194, 51],
]

round_key = [
    [173, 129, 68, 82],
    [223, 100, 38, 109],
    [32, 189, 53, 8],
    [253, 48, 187, 78],
]

def matrix2bytes(matrix: list[list]) -> bytes:
    return bytes(sum(matrix, []))

def add_round_key(s: list[list], k: list[list]) -> bytes:
    return matrix2bytes([[sss ^ kkk for sss, kkk in zip(ss, kk)] for ss, kk in zip(s, k)]) 
    # matrix = [[] for _ in range(4)]
    # for i in range(4):
    #     for j in range(4):
    #         matrix[i].append(s[i][j] ^ k[i][j])
            
    # return matrix2bytes(matrix)

print(add_round_key(state, round_key))
