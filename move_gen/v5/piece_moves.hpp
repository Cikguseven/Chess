#pragma once
#include <cstdint>
#include <string_view>
#include "move_lookup.hpp"
#include "reference_magic.h"

typedef uint64_t U64;

// Trailing zero count to get index of bit
#define SquarePosition(b) __builtin_ctzll(b)

const U64 not_a_file = 0x7F7F7F7F7F7F7F7F;
const U64 not_h_file = 0xFEFEFEFEFEFEFEFE;
const U64 fourth_rank = 0xFF000000;
const U64 fifth_rank = 0xFF00000000;
const U64 white_en_passant_not_a = 0x7f00000000;
const U64 white_en_passant_not_h = 0xfe00000000;
const U64 black_en_passant_not_a = 0x7f000000;
const U64 black_en_passant_not_h = 0xfe000000;

U64 ActivePawnMoves(Board &state) {
  if (state.Turn) {
    U64 b = state.WPawn;

    return b << 9 & not_h_file & state.Black
           | b << 7 & not_a_file & state.Black
           | b << 8 & state.Empty
           | b << 16 & fourth_rank & state.Empty
           | state.EnPassant & (b >> 1 & white_en_passant_not_a | b << 1 & white_en_passant_not_h);
  }

  else {
    U64 b = state.BPawn;

    return b >> 9 & not_a_file & state.Black
           | b >> 7 & not_h_file & state.Black
           | b >> 8 & state.Empty
           | b >> 16 & fifth_rank & state.Empty
           | state.EnPassant & (b >> 1 & black_en_passant_not_a | b << 1 & black_en_passant_not_h);
  }
}

U64 PassivePawnMoves(Board &state) {
  if (state.Turn)
    return state.BPawn >> 9 & not_a_file | state.BPawn >> 7 & not_h_file;
  else
    return state.WPawn << 9 & not_h_file | state.WPawn << 7 & not_a_file;
}

U64 ActiveKnightMoves(Board &state) {
  U64 b = state.Turn ? state.WKnight : state.BKnight;
  U64 not_team = state.Turn ? ~state.White : ~state.Black;

  return KnightMoves[SquarePosition(b)] & not_team;
}

U64 PassiveKnightMoves(Board &state) {
  U64 b = state.Turn ? state.BKnight : state.WKnight;

  return KnightMoves[SquarePosition(b)];
}

U64 ActiveKingMoves(Board &state) {
  U64 b = state.Turn ? state.WKing : state.BKing;
  U64 not_team = state.Turn ? ~state.White : ~state.Black;

  return KingMoves[SquarePosition(b)] & not_team;
}

U64 PassiveKingMoves(Board &state) {
  U64 b = state.Turn ? state.BKing : state.WKing;

  return KingMoves[SquarePosition(b)];
}

U64 ActiveBishopMoves(Board &state) {
  U64 b = state.Turn ? state.WBishop : state.BBishop;
  U64 not_team = state.Turn ? ~state.White : ~state.Black;
  U64 occupied = state.Occupied;

  return BishopMoves(SquarePosition(b), occupied) & not_team;
}

U64 PassiveBishopMoves(Board &state) {
  U64 b = state.Turn ? state.BBishop : state.WBishop;
  U64 not_team = state.Turn ? ~state.White : ~state.Black;
  U64 occupied = state.Occupied;

  return BishopMoves(SquarePosition(b), occupied) & not_team;
}