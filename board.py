import pieces

# from pprint import pprint

import pygame


def Board():
    skeleton = [[None for j in range(8)] for i in range(8)]
    for i in range(8):
        skeleton[1][i] = pieces.Pawn(-1, 7, i)
        skeleton[6][i] = pieces.Pawn(1, 2, i)
    '''
        if i == 0 or i == 7:
            skeleton[0][i] += 'R'
            skeleton[7][i] += 'R'
        if i == 1 or i == 6:
            skeleton[0][i] += 'N'
            skeleton[7][i] += 'N'
        if i == 2 or i == 5:
            skeleton[0][i] += 'B'
            skeleton[7][i] += 'B'
        if i == 3:
            skeleton[0][i] += 'Q'
            skeleton[7][i] += 'Q'
        if i == 4:
            skeleton[0][i] += 'K'
            skeleton[7][i] += 'K'
    '''
    return skeleton


def chessboard_bg(width):
    chessboard = pygame.image.load('./Images/Chessboard v3.png').convert()
    chessboard = pygame.transform.scale(chessboard, [width, width])
    return chessboard


def board_coordinates():
    nested_board_coordinates = [[] for i in range(8)]

    # Decimal coordinates of chess sprites to 5 decimal places
    def dc(n):
        return round((2 / 44 + n * 5 / 44), 5)

    for i in range(8):
        for j in range(8):
            nested_board_coordinates[i].append((dc(j), dc(i)))
    return nested_board_coordinates


def chess
