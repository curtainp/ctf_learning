import os

class ARC4:
    def __init__(self, key):
        self.S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + self.S[i] + key[i % len(key)]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
        self.i = 0
        self.j = 0

    def generate(self, n):
        out = []
        for _ in range(n):
            self.i = (self.i + 1) % 256
            self.j = (self.j + self.S[self.i]) % 256
            self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]
            k = self.S[(self.S[self.i] + self.S[self.j]) % 256]
            out.append(k)
        return out


class JSRandom:
    def __init__(self, seed):
        # 处理种子为字节数组，并添加终止符
        if isinstance(seed, str):
            key = list(seed.encode('utf-8')) + [0]
        elif isinstance(seed, int):
            key = []
            seed = seed & 0xFFFFFFFFFFFFFFFF  # 确保为64位整数
            for _ in range(8):
                key.append(seed & 0xFF)
                seed >>= 8
            key = key[::-1]  # 大端序
            key += [0]
        else:
            raise TypeError("Seed must be str or int")
        
        # 使用ARC4生成初始状态
        arc4 = ARC4(key)
        bytes_ = arc4.generate(16)  # 生成16个字节用于4个32位整数
        
        state = []
        for i in range(0, 16, 4):
            # 小端序组合32位整数
            chunk = bytes_[i:i+4]
            num = chunk[0] | (chunk[1] << 8) | (chunk[2] << 16) | (chunk[3] << 24)
            state.append(num)
        
        # 组合为两个64位的state0和state1
        self.state0 = (state[1] << 32) | state[0]
        self.state1 = (state[3] << 32) | state[2]

    def random(self):
        s0 = self.state0
        s1 = self.state1
        
        # Xorshift128+算法步骤
        s1 ^= (s1 << 23) & 0xFFFFFFFFFFFFFFFF
        s1 ^= (s1 >> 17)
        s1 ^= s0
        s1 ^= (s0 >> 26)
        
        # 更新状态
        self.state0 = self.state1
        self.state1 = s1
        
        # 生成随机数并转换为[0, 1)的浮点数
        random_num = (self.state0 + s0) & 0xFFFFFFFFFFFFFFFF
        return random_num / (1 << 64)

def main():
    seed = os.path.getmtime('./innov8_excav8/output.txt')
    rng = JSRandom(1741808274)

    print(rng.random())

main()
