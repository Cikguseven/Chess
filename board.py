import pieces

import pygame


# Initialises position from Forsyth–Edwards Notation (FEN)
def board(fen):

    board = [[fen[(8 * i) + j] for j in range(8)] for i in range(8)]

    piece_id = {'p': 'Pawn', 'n': 'Knight', 'b': 'Bishop',
                'r': 'Rook', 'q': 'Queen', 'k': 'King'}

    for i in board:
        for j in i:
            a = board.index(i)
            b = i.index(j)
            if not j.isdigit():
                if j.isupper():
                    team = 1
                else:
                    team = -1
                board[a][b] = getattr(pieces, piece_id[j.lower()])(
                    team, board.index(i), i.index(j))
            else:
                board[a][b] = None

    return board

# Displays image of chessboard


def chessboard_bg(width):

    chessboard = pygame.image.load('./Images/Chessboard v3.png').convert()
    chessboard = pygame.transform.scale(chessboard, (width, width))
    return chessboard


# Returns x & y coordinates of squares on board
def board_coordinates():

    # Decimal coordinates of chess sprites to nearest integer
    def dc(n):
        return round((2 / 44 + n * 5 / 44), 3)

    bc = [[None for j in range(8)] for i in range(8)]
    for i in range(8):
        for j in range(8):
            a = [dc(j), dc(i)]
            bc[i][j] = [round(880 * k) for k in a]
    return bc


# Displays pieces based on current position
def display_state(screen, state, bc, ps):

    for a, i in zip(state, bc):
        for b, j in zip(a, i):
            if b:
                image = pygame.image.load(b.filename() + b.id + '.png')
                image = pygame.transform.scale(image, ps)
                screen.blit(image, j)


# Converts mouse click coordinates to grid row/column no.
def grid(n):

    if 40 <= n <= 840:
        return ((n - 40) // 100)


def algebraic_notation(current_move):
    pass
    '''
    an = ''
    if current_move[0] != 'P':
        an += current_move[0]
    '''
