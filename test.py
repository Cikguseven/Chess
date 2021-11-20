from pprint import pprint

nested_algebraic_board = [[] for i in range(8)]

for i in range(8):
    for j in range(97, 105):
        nested_algebraic_board[i].append(chr(j) + str(8 - i))

nested_board_coordinates = [[] for i in range(8)]


def dc(n):
    return round((2 / 44 + n * 5 / 44), 5)


for i in range(8):
    for j in range(8):
        nested_board_coordinates[i].append((dc(j), dc(i)))

pprint(nested_algebraic_board)

pprint(nested_board_coordinates)
