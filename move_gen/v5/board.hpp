#include <cstdint>
#include <bitset>
#include <string_view>
using namespace std;

typedef uint64_t u64;

void BmpPrint(u64 bitmap) {

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

u64 BmpGen(string_view FEN, char p) {
  int i = 0;
  char c{};
  int counter = 63;
  u64 result = 0;

  while ((c = FEN[i++]) != ' ')
  {
    u64 P = 1ull << counter;
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

u64 GameState(string_view FEN, char a) {
  int i = 0;
  char c{};
  u64 result = 0;

  while (FEN[i++] != ' ') {

  }

  char wb = FEN[i++];

  if (a == 't') {
    if (wb == 'w') return true;
    else return false;
  }

  i++;

  
  while ((c = FEN[i++]) != ' ') {
    if (a == 'c'){
      switch (c) {
        case 'K': result |= 1ull << 1; break;
        case 'Q': result |= 1ull << 5; break;
        case 'k': result |= 1ull << 57; break;
        case 'q': result |= 1ull << 61; break;
      }
    }
  }

  if (a == 'c') return result;
  else u64 result = 0;

  char ep = FEN[i++];

  if (ep != '-') {
    if (wb == 'w') return 1ull << 40 + 'a' - (int)ep;    
    else return 1ull << 32 + 'a' - (int)ep;
  }

  return 0;
}

struct Board {
  u64 BPawn;
  u64 BKnight;
  u64 BBishop;
  u64 BRook;
  u64 BQueen;
  u64 BKing;

  u64 WPawn;
  u64 WKnight;
  u64 WBishop;
  u64 WRook;
  u64 WQueen;
  u64 WKing;

  u64 Black;
  u64 White;
  u64 Occupied;
  u64 Empty;

  u64 Castling;
  u64 EnPassant;
  bool Turn;

  Board(
    u64 bp, u64 bn, u64 bb, u64 br, u64 bq, u64 bk,
    u64 wp, u64 wn, u64 wb, u64 wr, u64 wq, u64 wk,
    u64 cs, u64 ep, bool turn) :
    BPawn(bp), BKnight(bn), BBishop(bb), BRook(br), BQueen(bq), BKing(bk),
    WPawn(wp), WKnight(wn), WBishop(wb), WRook(wr), WQueen(wq), WKing(wk),
    Black(bp | bn | bb | br | bq | bk),
    White(wp | wn | wb | wr | wq | wk),
    Occupied(Black | White),
    Empty(~Occupied),
    Castling(cs),
    EnPassant(ep),
    Turn(turn)
  {

  }

  Board(string_view FEN) :
    Board(BmpGen(FEN, 'p'), BmpGen(FEN, 'n'), BmpGen(FEN, 'b'),
          BmpGen(FEN, 'r'), BmpGen(FEN, 'q'), BmpGen(FEN, 'k'),
          BmpGen(FEN, 'P'), BmpGen(FEN, 'N'), BmpGen(FEN, 'B'),
          BmpGen(FEN, 'R'), BmpGen(FEN, 'Q'), BmpGen(FEN, 'K'),
          GameState(FEN, 'c'), GameState(FEN, 'e'), GameState(FEN, 't'))
  {

  }
};

