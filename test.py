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
