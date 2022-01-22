#include <iostream>
#include <string>
#include "board.hpp"
#include "piece_moves.hpp"
using namespace std;

int main() {

  string raw_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";

  Board bmp(raw_fen);

  BmpPrint(bmp.White);
  BmpPrint(bmp.Black);

  // BmpPrint(WPawnAttackLeft);
  // BmpPrint(WPawnAttackRight);
  // BmpPrint(WPawnForward);
  // BmpPrint(WPawnForwardTwice);

  return 0;
}