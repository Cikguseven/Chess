#include <cstdint>
#include <bitset>
#include <string_view>

typedef uint64_t u64;

const u64 not_a_file = 0x7F7F7F7F7F7F7F7F;
const u64 not_ab_file = 0x3F3F3F3F3F3F3F3F;
const u64 not_gh_file = 0xFCFCFCFCFCFCFCFC;
const u64 not_h_file = 0xFEFEFEFEFEFEFEFE;
const u64 fourth_rank = 0xFF000000;
const u64 fifth_rank = 0xFF00000000;
const u64 white_en_passant_not_a = 0x7f00000000;
const u64 white_en_passant_not_h = 0xfe00000000;
const u64 black_en_passant_not_a = 0x7f000000;
const u64 black_en_passant_not_h = 0xfe000000;

u64 ActivePawnMoves(Board state) {
  u64 result = 0;
  if (state.Turn) {
    u64 b = state.WPawn;

    return b << 9 & not_h_file & state.Black
           | b << 7 & not_a_file & state.Black
           | b << 8 & state.Empty
           | b << 16 & fourth_rank & state.Empty
           | state.EnPassant & (b >> 1 & white_en_passant_not_a | b << 1 & white_en_passant_not_h);
  }

  else {
    u64 b = state.BPawn;

    return b >> 9 & not_a_file & state.Black
           | b >> 7 & not_h_file & state.Black
           | b >> 8 & state.Empty
           | b >> 16 & fifth_rank & state.Empty
           | state.EnPassant & (b >> 1 & black_en_passant_not_a | b << 1 & black_en_passant_not_h);
  }
}

u64 PassivePawnMoves(Board state) {
  if (state.Turn)
    return state.BPawn >> 9 & not_a_file | state.BPawn >> 7 & not_h_file;
  else
    return state.WPawn << 9 & not_h_file | state.WPawn << 7 & not_a_file;
}

u64 ActiveKnightMoves(Board state) {
  u64 b;
  u64 not_team;

  if (state.Turn) {
    b = state.WKnight;
    not_team = ~state.White;
  }
  else {
    b = state.BKnight;
    not_team = ~state.Black;
  }

  return (b << 17 & not_h_file | b << 15 & not_a_file | b << 10 & not_gh_file
          | b << 6 & not_ab_file | b >> 6 & not_gh_file | b >> 10 & not_ab_file
          | b >> 15 & not_h_file | b >> 17 & not_a_file) & not_team;
}

u64 PassiveKnightMoves(Board state) {
  u64 b;

  if (state.Turn) b = state.BKnight;
  else b = state.WKnight;

  return b << 17 & not_h_file | b << 15 & not_a_file | b << 10 & not_gh_file
         | b << 6 & not_ab_file | b >> 6 & not_gh_file | b >> 10 & not_ab_file
         | b >> 15 & not_h_file | b >> 17 & not_a_file;
}

u64 ActiveKingMoves(Board state) {
  u64 b;
  u64 not_team;

  if (state.Turn) {
    b = state.WKing;
    not_team = ~state.White;
  }
  else {
    b = state.BKing;
    not_team = ~state.Black;
  }

  return (b << 9 & not_h_file | b << 8 | b << 7 & not_a_file
          | b << 1 & not_h_file | b >> 1 & not_a_file | b >> 7 & not_h_file
          | b >> 8 | b >> 9 & not_a_file) & not_team;
}

u64 PassiveKingMoves(Board state) {
  u64 b;

  if (state.Turn) b = state.BKing;
  else b = state.WKing;

  return b << 9 & not_h_file | b << 8 | b << 7 & not_a_file
         | b << 1 & not_h_file | b >> 1 & not_a_file | b >> 7 & not_h_file
         | b >> 8 | b >> 9 & not_a_file;
}
