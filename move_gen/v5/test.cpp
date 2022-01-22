#include <iostream>
#include <bitset>
using namespace std;

int main()
{
  unsigned short b = 65535;

  bitset<15> a(b);

  cout << a << endl;

  b <<= 1;

  cout << b << endl;

  return 0;
}