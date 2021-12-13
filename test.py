'''
from pprint import pprint

nested_algebraic_board = [[] for i in range(8)]

for i in range(8):
    for j in range(97, 105):
        nested_algebraic_board[i].append(chr(j) + str(8 - i))

pprint(nested_algebraic_board)


def dc(n):
    return round((2 / 44 + n * 5 / 44), 3)


nested_board_coordinates = [[None for j in range(8)] for i in range(8)]

for i in range(8):
    for j in range(8):
        a = [dc(j), dc(i)]
        nested_board_coordinates[i][j] = [round(880 * k) for k in a]

pprint(nested_board_coordinates)
'''

'''
def fen():
    fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq b6 0 1'

    info_dict = {'turn': 1, 'castling': [], 'en_passant': None}

    for i in fen:
        if i == ' ':
            break
        elif i.isdigit():
            fen = fen.replace(i, int(i) * '0')

    fen = fen.replace('/', '')

    if fen[-5] == '3' or fen[-5] == '6':
        a = str(ord(fen[-6]) - 97)
        if fen[65] == 'b' and fen[-5] == '3':
            info_dict['turn'] = -1
            info_dict['en_passant'] = 'P6' + a + '4' + a
        elif fen[65] == 'w' and fen[-5] == '6':
            info_dict['en_passant'] = 'P1' + a + '3' + a

    a = {'K': '76', 'Q': '72', 'k': '06', 'q': '02'}
    i = 67

    while True:
        j = fen[i]
        if j == ' ' or j == '-':
            break
        elif j in a:
            info_dict['castling'].append(a[j])
            i += 1

    return fen, info_dict


print(fen()[1])
'''

fen = 'r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1'

for i in fen:
    print(i)
    if i.isspace():
        break
    elif i.isdigit():
        fen.index(i) = str(int(i) * 0)
        
print(fen)