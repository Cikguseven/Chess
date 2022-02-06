/**************************************\
 ======================================

         Plain magic bitboards
     implementation & demonstration

                  by

           Code Monkey King

 ======================================
\**************************************/

// system headers
#pragma once
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
using namespace std;

// define bitboard type
typedef uint64_t U64;

// bits manipulations
#define get_bit(bitboard, square) (bitboard & (1ULL << square))
#define set_bit(bitboard, square) (bitboard |= (1ULL << square))
#define pop_bit(bitboard, square) (get_bit(bitboard, square) ? (bitboard ^= (1ULL << square)) : 0)

// square encoding using little endian rank, big endian file mode
enum {
  h1, g1, f1, e1, d1, c1, b1, a1,
  h2, g2, f2, e2, d2, c2, b2, a2,
  h3, g3, f3, e3, d3, c3, b3, a3,
  h4, g4, f4, e4, d4, c4, b4, a4,
  h5, g5, f5, e5, d5, c5, b5, a5,
  h6, g6, f6, e6, d6, c6, b6, a6,
  h7, g7, f7, e7, d7, c7, b7, a7,
  h8, g8, f8, e8, d8, c8, b8, a8
};

// rook & bishop flags
enum {rook, bishop};

// rook relevant occupancy bits
static constexpr int rook_relevant_bits[64] = {
  12, 11, 11, 11, 11, 11, 11, 12,
  11, 10, 10, 10, 10, 10, 10, 11,
  11, 10, 10, 10, 10, 10, 10, 11,
  11, 10, 10, 10, 10, 10, 10, 11,
  11, 10, 10, 10, 10, 10, 10, 11,
  11, 10, 10, 10, 10, 10, 10, 11,
  11, 10, 10, 10, 10, 10, 10, 11,
  12, 11, 11, 11, 11, 11, 11, 12
};

// bishop relevant occupancy bits
static constexpr int bishop_relevant_bits[64] = {
  6, 5, 5, 5, 5, 5, 5, 6,
  5, 5, 5, 5, 5, 5, 5, 5,
  5, 5, 7, 7, 7, 7, 5, 5,
  5, 5, 7, 9, 9, 7, 5, 5,
  5, 5, 7, 9, 9, 7, 5, 5,
  5, 5, 7, 7, 7, 7, 5, 5,
  5, 5, 5, 5, 5, 5, 5, 5,
  6, 5, 5, 5, 5, 5, 5, 6
};

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

  // otherwise
  else
    // return illegal index
    return -1;
}

// set occupancies
U64 set_occupancy(int index, int bits_in_mask, U64 attack_mask)
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
  return occupancy;
}

// bishop attacks
U64 bishop_attacks_on_the_fly(int square, U64 block)
{
  // attack bitboard
  U64 attacks = 0ULL;

  // init files & ranks
  int f, r;

  // init target files & ranks
  int tr = square / 8;
  int tf = square % 8;

  // generate attacks
  for (r = tr + 1, f = tf + 1; r <= 7 && f <= 7; r++, f++)
  {
    attacks |= (1ULL << (r * 8 + f));
    if (block & (1ULL << (r * 8 + f))) break;
  }

  for (r = tr + 1, f = tf - 1; r <= 7 && f >= 0; r++, f--)
  {
    attacks |= (1ULL << (r * 8 + f));
    if (block & (1ULL << (r * 8 + f))) break;
  }

  for (r = tr - 1, f = tf + 1; r >= 0 && f <= 7; r--, f++)
  {
    attacks |= (1ULL << (r * 8 + f));
    if (block & (1ULL << (r * 8 + f))) break;
  }

  for (r = tr - 1, f = tf - 1; r >= 0 && f >= 0; r--, f--)
  {
    attacks |= (1ULL << (r * 8 + f));
    if (block & (1ULL << (r * 8 + f))) break;
  }

  // return attack map for bishop on a given square
  return attacks;
}

// rook attacks
U64 rook_attacks_on_the_fly(int square, U64 block)
{
  // attacks bitboard
  U64 attacks = 0ULL;

  // init files & ranks
  int f, r;

  // init target files & ranks
  int tr = square / 8;
  int tf = square % 8;

  // generate attacks
  for (r = tr + 1; r <= 7; r++)
  {
    attacks |= (1ULL << (r * 8 + tf));
    if (block & (1ULL << (r * 8 + tf))) break;
  }

  for (r = tr - 1; r >= 0; r--)
  {
    attacks |= (1ULL << (r * 8 + tf));
    if (block & (1ULL << (r * 8 + tf))) break;
  }

  for (f = tf + 1; f <= 7; f++)
  {
    attacks |= (1ULL << (tr * 8 + f));
    if (block & (1ULL << (tr * 8 + f))) break;
  }

  for (f = tf - 1; f >= 0; f--)
  {
    attacks |= (1ULL << (tr * 8 + f));
    if (block & (1ULL << (tr * 8 + f))) break;
  }

  // return attack map for bishop on a given square
  return attacks;
}

// attacks
U64 bishop_attacks[64][512];
U64 rook_attacks[64][4096];

// mask
static constexpr U64 bishop_mask[64] = {
  0x40201008040200, 0x00402010080400, 0x00004020100A00,
  0x00000040221400, 0x00000002442800, 0x00000204085000,
  0x00020408102000, 0x02040810204000, 0x20100804020000,
  0x40201008040000, 0x004020100A0000, 0x00004022140000,
  0x00000244280000, 0x00020408500000, 0x02040810200000,
  0x04081020400000, 0x10080402000200, 0x20100804000400,
  0x4020100A000A00, 0x00402214001400, 0x00024428002800,
  0x02040850005000, 0x04081020002000, 0x08102040004000,
  0x08040200020400, 0x10080400040800, 0x20100A000A1000,
  0x40221400142200, 0x02442800284400, 0x04085000500800,
  0x08102000201000, 0x10204000402000, 0x04020002040800,
  0x08040004081000, 0x100A000A102000, 0x22140014224000,
  0x44280028440200, 0x08500050080400, 0x10200020100800,
  0x20400040201000, 0x02000204081000, 0x04000408102000,
  0x0A000A10204000, 0x14001422400000, 0x28002844020000,
  0x50005008040200, 0x20002010080400, 0x40004020100800,
  0x00020408102000, 0x00040810204000, 0x000A1020400000,
  0x00142240000000, 0x00284402000000, 0x00500804020000,
  0x00201008040200, 0x00402010080400, 0x02040810204000,
  0x04081020400000, 0x0A102040000000, 0x14224000000000,
  0x28440200000000, 0x50080402000000, 0x20100804020000,
  0x40201008040200
};

static constexpr U64 rook_mask[64] = {
  0x000101010101017E, 0x000202020202027C, 0x000404040404047A,
  0x0008080808080876, 0x001010101010106E, 0x002020202020205E,
  0x004040404040403E, 0x008080808080807E, 0x0001010101017E00,
  0x0002020202027C00, 0x0004040404047A00, 0x0008080808087600,
  0x0010101010106E00, 0x0020202020205E00, 0x0040404040403E00,
  0x0080808080807E00, 0x00010101017E0100, 0x00020202027C0200,
  0x00040404047A0400, 0x0008080808760800, 0x00101010106E1000,
  0x00202020205E2000, 0x00404040403E4000, 0x00808080807E8000,
  0x000101017E010100, 0x000202027C020200, 0x000404047A040400,
  0x0008080876080800, 0x001010106E101000, 0x002020205E202000,
  0x004040403E404000, 0x008080807E808000, 0x0001017E01010100,
  0x0002027C02020200, 0x0004047A04040400, 0x0008087608080800,
  0x0010106E10101000, 0x0020205E20202000, 0x0040403E40404000,
  0x0080807E80808000, 0x00017E0101010100, 0x00027C0202020200,
  0x00047A0404040400, 0x0008760808080800, 0x00106E1010101000,
  0x00205E2020202000, 0x00403E4040404000, 0x00807E8080808000,
  0x007E010101010100, 0x007C020202020200, 0x007A040404040400,
  0x0076080808080800, 0x006E101010101000, 0x005E202020202000,
  0x003E404040404000, 0x007E808080808000, 0x7E01010101010100,
  0x7C02020202020200, 0x7A04040404040400, 0x7608080808080800,
  0x6E10101010101000, 0x5E20202020202000, 0x3E40404040404000,
  0x7E80808080808000
};

// bishop magic number
static constexpr U64 bishop_magics[64] = {
  0x89A1121896040240ULL, 0x2004844802002010ULL, 0x2068080051921000ULL, 
  0x62880A0220200808ULL, 0x0004042004000000ULL, 0x0100822020200011ULL, 
  0xC00444222012000AULL, 0x0028808801216001ULL, 0x0400492088408100ULL, 
  0x0201C401040C0084ULL, 0x00840800910A0010ULL, 0x0000082080240060ULL, 
  0x2000840504006000ULL, 0x30010C4108405004ULL, 0x1008005410080802ULL, 
  0x8144042209100900ULL, 0x0208081020014400ULL, 0x004800201208CA00ULL, 
  0x0F18140408012008ULL, 0x1004002802102001ULL, 0x0841000820080811ULL, 
  0x0040200200A42008ULL, 0x0000800054042000ULL, 0x88010400410C9000ULL, 
  0x0520040470104290ULL, 0x1004040051500081ULL, 0x2002081833080021ULL, 
  0x000400C00C010142ULL, 0x941408200C002000ULL, 0x0658810000806011ULL, 
  0x0188071040440A00ULL, 0x4800404002011C00ULL, 0x0104442040404200ULL, 
  0x0511080202091021ULL, 0x0004022401120400ULL, 0x80C0040400080120ULL, 
  0x8040010040820802ULL, 0x0480810700020090ULL, 0x0102008E00040242ULL, 
  0x0809005202050100ULL, 0x8002024220104080ULL, 0x0431008804142000ULL, 
  0x0019001802081400ULL, 0x0200014208040080ULL, 0x3308082008200100ULL, 
  0x041010500040C020ULL, 0x4012020C04210308ULL, 0x208220A202004080ULL, 
  0x0111040120082000ULL, 0x6803040141280A00ULL, 0x2101004202410000ULL, 
  0x8200000041108022ULL, 0x0000021082088000ULL, 0x0002410204010040ULL, 
  0x0040100400809000ULL, 0x0822088220820214ULL, 0x0040808090012004ULL, 
  0x00910224040218C9ULL, 0x0402814422015008ULL, 0x0090014004842410ULL, 
  0x0001000042304105ULL, 0x0010008830412A00ULL, 0x2520081090008908ULL, 
  0x40102000A0A60140ULL
};

// rook magic numbers
static constexpr U64 rook_magics[64] = {
  0x0A8002C000108020ULL, 0x06C00049B0002001ULL, 0x0100200010090040ULL, 
  0x2480041000800801ULL, 0x0280028004000800ULL, 0x0900410008040022ULL, 
  0x0280020001001080ULL, 0x2880002041000080ULL, 0xA000800080400034ULL, 
  0x0004808020004000ULL, 0x2290802004801000ULL, 0x0411000D00100020ULL, 
  0x0402800800040080ULL, 0x000B000401004208ULL, 0x2409000100040200ULL, 
  0x0001002100004082ULL, 0x0022878001E24000ULL, 0x1090810021004010ULL, 
  0x0801030040200012ULL, 0x0500808008001000ULL, 0x0A08018014000880ULL, 
  0x8000808004000200ULL, 0x0201008080010200ULL, 0x0801020000441091ULL, 
  0x0000800080204005ULL, 0x1040200040100048ULL, 0x0000120200402082ULL, 
  0x0D14880480100080ULL, 0x0012040280080080ULL, 0x0100040080020080ULL, 
  0x9020010080800200ULL, 0x0813241200148449ULL, 0x0491604001800080ULL, 
  0x0100401000402001ULL, 0x4820010021001040ULL, 0x0400402202000812ULL, 
  0x0209009005000802ULL, 0x0810800601800400ULL, 0x4301083214000150ULL, 
  0x204026458E001401ULL, 0x0040204000808000ULL, 0x8001008040010020ULL, 
  0x8410820820420010ULL, 0x1003001000090020ULL, 0x0804040008008080ULL, 
  0x0012000810020004ULL, 0x1000100200040208ULL, 0x430000A044020001ULL, 
  0x0280009023410300ULL, 0x00E0100040002240ULL, 0x0000200100401700ULL, 
  0x2244100408008080ULL, 0x0008000400801980ULL, 0x0002000810040200ULL, 
  0x8010100228810400ULL, 0x2000009044210200ULL, 0x4080008040102101ULL, 
  0x0040002080411D01ULL, 0x2005524060000901ULL, 0x0502001008400422ULL, 
  0x489A000810200402ULL, 0x0001004400080A13ULL, 0x4000011008020084ULL, 
  0x0026002114058042ULL
};

// init slider pieces attacks
void init_sliders_attacks(int is_bishop)
{
  // loop over 64 board squares
  for (int square = 0; square < 64; square++)
  {
    // init current mask
    U64 mask = is_bishop ? bishop_mask[square] : rook_mask[square];

    // count attack mask bits
    int bit_count = count_bits(mask);

    // occupancy variations count
    int occupancy_variations = 1 << bit_count;

    // loop over occupancy variations
    for (int count = 0; count < occupancy_variations; count++)
    {
      // bishop
      if (is_bishop)
      {
        // init occupancies, magic index & attacks
        U64 occupancy = set_occupancy(count, bit_count, mask);
        U64 magic_index = occupancy * bishop_magics[square] >> 64 - bishop_relevant_bits[square];
        bishop_attacks[square][magic_index] = bishop_attacks_on_the_fly(square, occupancy);
      }

      // rook
      else
      {
        // init occupancies, magic index & attacks
        U64 occupancy = set_occupancy(count, bit_count, mask);
        U64 magic_index = occupancy * rook_magics[square] >> 64 - rook_relevant_bits[square];
        rook_attacks[square][magic_index] = rook_attacks_on_the_fly(square, occupancy);
      }
    }
  }
}

// lookup bishop attacks
U64 BishopMoves(int square, U64 occupancy) {

  // calculate magic index
  occupancy &= bishop_mask[square];
  occupancy *=  bishop_magics[square];
  occupancy >>= 64 - bishop_relevant_bits[square];

  // return relevant attacks
  return bishop_attacks[square][occupancy];

}

// lookup rook attacks
U64 RookMoves(int square, U64 occupancy) {

  // calculate magic index
  occupancy &= rook_mask[square];
  occupancy *=  rook_magics[square];
  occupancy >>= 64 - rook_relevant_bits[square];

  // return relevant attacks
  return rook_attacks[square][occupancy];
}
