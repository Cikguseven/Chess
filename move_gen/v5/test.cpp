#include <iostream>
#include <cstdint>
#include <bitset>
using namespace std;

typedef uint64_t U64;

#define get_bit(bitboard, square) (bitboard & (1ULL << square))
#define set_bit(bitboard, square) (bitboard |= (1ULL << square))
#define pop_bit(bitboard, square) (get_bit(bitboard, square) ? (bitboard ^= (1ULL << square)) : 0)

void BmpPrint(const U64 &bitmap) {

  bitset<64> bin_str(bitmap);

  for (int i = 63; i >= 0; --i) {
    if (bin_str[i])
      cout << '1';
    else
      cout << '.';
    if (!(i % 8))
      cout << endl;
  }
  cout << endl;
}

// count bits (Brian Kernighan's way)
int count_bits(U64 bitboard) {
  // bit count
  int count = 0;

  // pop bits untill bitboard is empty
  while (bitboard)
  {
    // increment count
    count++;

    // consecutively reset least significant 1st bit
    bitboard &= bitboard - 1;
  }

  // return bit count
  return count;
}

// get index of LS1B in bitboard
int get_ls1b_index(U64 bitboard) {
  // make sure bitboard is not empty
  if (bitboard != 0)
    // convert trailing zeros before LS1B to ones and count them
    return count_bits((bitboard & -bitboard) - 1);
}

void set_occupancy(int index, int bits_in_mask, U64 attack_mask)
{
    // occupancy map
    U64 occupancy = 0ULL;

    // loop over the range of bits within attack mask
    for (int count = 0; count < bits_in_mask; count++)
    {
        // get LS1B index of attacks mask
        int square = get_ls1b_index(attack_mask);

        // pop LS1B in attack map
        pop_bit(attack_mask, square);

        // make sure occupancy is on board
        if (index & (1 << count))
            // populate occupancy map
            occupancy |= (1ULL << square);
    }

    // return occupancy map
    BmpPrint(occupancy);
}

int main() {

  U64 b = 1111ULL;

  // get_ls1b_index(263168);

  for (int i = 0; i < 16; i++) {
    set_occupancy(i, 4, b);
    cout << i << endl;
  }

  return 0;
};