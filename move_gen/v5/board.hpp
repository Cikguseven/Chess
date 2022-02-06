#pragma once
#include <cstdint>
#include <string_view>
#include <tuple>
using namespace std;

typedef uint64_t U64;

#define get_bit(bitboard, square) (bitboard & (1ULL << square))

void PrintBitboard(U64 bitboard)
{
    // loop over board ranks
    for (int rank = 7; rank >= 0; --rank)
    {
        // loop over board files
        for (int file = 7; file >= 0; --file)
        {
            // init board square
            int square = rank * 8 + file;

            // print ranks
            if (file == 7)
                cout << rank + 1 << "   ";

            char x = get_bit(bitboard, square) ? '1' : '.';

            // print bit indexed by board square
            cout << x << " ";
        }

        cout << endl;
    }

    // print files
    cout << endl << "    a b c d e f g h" << endl << endl;
}

U64 BmpGen(const string_view &FEN, char p) {
  int i = 0;
  char c{};
  int counter = 63;
  U64 result = 0;

  while ((c = FEN[i++]) != ' ')
  {
    U64 P = 1ull << counter;
    switch (c) {
    case '/': counter += 1; break;
    case '1': break;
    case '2': counter -= 1; break;
    case '3': counter -= 2; break;
    case '4': counter -= 3; break;
    case '5': counter -= 4; break;
    case '6': counter -= 5; break;
    case '7': counter -= 6; break;
    case '8': counter -= 7; break;
    default:
      if (c == p) result |= P; //constexpr parsing happens here
    }
    counter--;
  }
  return result;
}

tuple<bool, U64, U64> GameState(const string_view FEN) {
  bool turn = false;
  U64 castling = 0;
  U64 en_passant = 0;

  int i = FEN.find(' ');

  char wb = FEN[++i];

  if (wb == 'w') turn = true;

  ++i;

  char c{};

  while ((c = FEN[i++]) != ' ') {
    switch (c) {
    case 'K': castling = 1ull << 1; break;
    case 'Q': castling |= 1ull << 5; break;
    case 'k': castling |= 1ull << 57; break;
    case 'q': castling |= 1ull << 61; break;
    }
  }

  char ep = FEN[i++];

  if (ep != '-') {
    if (wb == 'w') en_passant = 1ull << (40 + 'a' - (int)ep);
    else en_passant = 1ull << (32 + 'a' - (int)ep);
  }

  return make_tuple(turn, castling, en_passant);
}

struct Board {
  U64 BPawn;
  U64 BKnight;
  U64 BBishop;
  U64 BRook;
  U64 BQueen;
  U64 BKing;

  U64 WPawn;
  U64 WKnight;
  U64 WBishop;
  U64 WRook;
  U64 WQueen;
  U64 WKing;

  U64 Black;
  U64 White;
  U64 Occupied;
  U64 Empty;

  bool Turn;
  U64 Castling;
  U64 EnPassant;
  
  Board(
    U64 bp, U64 bn, U64 bb, U64 br, U64 bq, U64 bk,
    U64 wp, U64 wn, U64 wb, U64 wr, U64 wq, U64 wk, string_view FEN) :
    BPawn(bp), BKnight(bn), BBishop(bb), BRook(br), BQueen(bq), BKing(bk),
    WPawn(wp), WKnight(wn), WBishop(wb), WRook(wr), WQueen(wq), WKing(wk),
    Black(bp | bn | bb | br | bq | bk),
    White(wp | wn | wb | wr | wq | wk),
    Occupied(Black | White),
    Empty(~Occupied)
  {
    tuple z = GameState(FEN);
    Turn = get<0>(z);
    Castling = get<1>(z);
    EnPassant = get<2>(z);
  }

  Board(string_view FEN) :
    Board(BmpGen(FEN, 'p'), BmpGen(FEN, 'n'), BmpGen(FEN, 'b'),
          BmpGen(FEN, 'r'), BmpGen(FEN, 'q'), BmpGen(FEN, 'k'),
          BmpGen(FEN, 'P'), BmpGen(FEN, 'N'), BmpGen(FEN, 'B'),
          BmpGen(FEN, 'R'), BmpGen(FEN, 'Q'), BmpGen(FEN, 'K'),
          FEN)
  {

  }
};
