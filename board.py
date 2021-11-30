import pieces

# from pprint import pprint

import pygame


def board():
    skeleton = [[None for j in range(8)] for i in range(8)]
    for i in range(8):
        skeleton[1][i] = pieces.Pawn(-1, 1, i)
        skeleton[6][i] = pieces.Pawn(1, 6, i)
        if i == 0 or i == 7:
            skeleton[0][i] = pieces.Rook(-1, 0, i)
            skeleton[7][i] = pieces.Rook(1, 7, i)
        if i == 1 or i == 6:
            skeleton[0][i] = pieces.Knight(-1, 0, i)
            skeleton[7][i] = pieces.Knight(1, 7, i)
        if i == 2 or i == 5:
            skeleton[0][i] = pieces.Bishop(-1, 0, i)
            skeleton[7][i] = pieces.Bishop(1, 7, i)
        if i == 3:
            skeleton[0][i] = pieces.Queen(-1, 0, i)
            skeleton[7][i] = pieces.Queen(1, 7, i)
        if i == 4:
            skeleton[0][i] = pieces.King(-1, 0, i)
            skeleton[7][i] = pieces.King(1, 7, i)
    return skeleton


def chessboard_bg(width):
    chessboard = pygame.image.load('./Images/Chessboard v3.png').convert()
    chessboard = pygame.transform.scale(chessboard, (width, width))
    return chessboard


def board_coordinates():
    nbc = [[None for j in range(8)] for i in range(8)]
    for i in range(8):
        for j in range(8):
            a = [dc(j), dc(i)]
            nbc[i][j] = [round(880 * k) for k in a]
    return nbc


def display_board(screen, width, sp, nbc):
    for a, i in zip(sp, nbc):
        for b, j in zip(a, i):
            if b:
                screen.blit(b.image, j)


# Decimal coordinates of chess sprites to 5 decimal places
def dc(n):
    return round((2 / 44 + n * 5 / 44), 3)


def row(n):
    if 40 <= n <= 840:
        return ((n - 40) // 100)
