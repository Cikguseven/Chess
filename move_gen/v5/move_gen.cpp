#include <iostream>
#include <string>
#include "board.hpp"
#include "piece_moves.hpp"
#include "reference_magic.h"

using namespace std;

int main() {

  init_sliders_attacks(bishop);
  init_sliders_attacks(rook);

  // const string raw_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";

  const string raw_fen = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RN1QK2R w KQ - 1 8";

  Board bmp(raw_fen);

  PrintBitboard(ActiveBishopMoves(bmp));

  // BmpPrint(WPawnAttackLeft);
  // BmpPrint(WPawnAttackRight);
  // BmpPrint(WPawnForward);
  // BmpPrint(WPawnForwardTwice);

  return 0;
}