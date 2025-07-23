https://beginner-ecb-a-tron-9000-1fc633e2ebf6.2025.ductf.net/

refer to: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_codebook_(ECB)

# ECB weakness

1. Deterministic: identical plaintext blocks will always produce identical ciphertext.
2. Block independence: each 16 bytes block is encrypted separately

so, with this challenge, the secret key is append to our input with block boundary, leverage this to brute-force secret key one by one.
