#include <stdint.h>

#define n 624
#define m 397
#define w 32
#define r 31
#define UMASK (0xffffffffUL << r)
#define LMASK (0xffffffffUL >> (w - r))
#define a 0x9908b0dfUL
#define u 11
#define s 7
#define t 15
#define l 18
#define b 0x9d2c5680UL
#define c 0xefc60000UL
#define f 1812433253UL

typedef struct {
  uint32_t state_array[n];
  int state_index;
} mt_state;

void initialize_state(mt_state *state, uint32_t seed) {
  uint32_t *state_array = &(state->state_array[0]);

  state_array[0] = seed;

  for (int i = 1; i < n; i++) {
    seed = f * (seed ^ (seed >> (w - 2))) + i;
    state_array[i] = seed;
  }
  state->state_index = 0;
}

uint32_t random_uint32(mt_state *state) {
  uint32_t *state_array = &(state->state_array[0]);

  int k = state->state_index;

  /* int k = k - n; */
  /* if (k < 0) k += n; */

  int j = k - (n - 1); /* point to state n - 1 iterations before */
  if (j < 0)
    j += n; /* modulo n circular indexing */

  uint32_t x = (state_array[k] & UMASK) | (state_array[j] & LMASK);

  uint32_t xA = x >> 1;
  if (x & 0x00000001UL)
    xA ^= a;

  j = k - (n - m);
  if (j < 0)
    j += n;

  x = state_array[j] ^ xA;
  state_array[k++] = x;

  if (k >= n)
    k = 0;
  state->state_index = k;

  uint32_t y = x ^ (x >> u);
  y = y ^ ((y << s) & b);
  y = y ^ ((y << t) & c);
  uint32_t z = y ^ (y >> 1);
  return z;
}
