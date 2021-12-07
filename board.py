import pieces

import pygame


# Initialises starting position of chess pieces
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


# Displays image of chessboard
def chessboard_bg(width):
    chessboard = pygame.image.load('./Images/Chessboard v4.png').convert()
    chessboard = pygame.transform.scale(chessboard, (width, width))
    return chessboard


# Returns x & y coordinates of squares on board
def board_coordinates():

    # Decimal coordinates of chess sprites to nearest integer
    def dc(n):
        return round((2 / 44 + n * 5 / 44), 3)

    nbc = [[None for j in range(8)] for i in range(8)]
    for i in range(8):
        for j in range(8):
            a = [dc(j), dc(i)]
            nbc[i][j] = [round(880 * k) for k in a]
    return nbc


# Displays pieces based on current position
def display_state(screen, state, nbc, ps):
    for a, i in zip(state, nbc):
        for b, j in zip(a, i):
            if b:
                image = pygame.image.load(b.filename() + b.id + '.png')
                image = pygame.transform.scale(image, ps)
                screen.blit(image, j)


# Returns row/column no. of grid
def grid(n):
    if 40 <= n <= 840:
        return ((n - 40) // 100)
