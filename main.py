import board
import pieces
import pygame

from copy import deepcopy


def main():
    pygame.init()

    def king_pos():
        if turn == 1:
            return wk_pos
        else:
            return bk_pos

    # Checks if move is legal (does not result in check)
    def legal_moves(x, y):
        legal_moves = []
        piece = state[y][x]
        castling = fen_info['castling']

        for i in piece.moves(state):
            kp = king_pos()
            state_copy = deepcopy(state)
            j, k = int(i[0]), int(i[1])
            # Removes king capturing moves
            if not hasattr(state_copy[j][k], 'immune'):

                # Test if new position results in check
                state_copy[j][k] = state_copy[y][x]
                state_copy[y][x] = None
                if state_copy[j][k].id == 'K':

                    # Enables castling
                    if abs(x - k) == 2:
                        if (i in castling and not in_check(state, kp)
                            and str(y) + str((x + k) // 2) in legal_moves
                                and not in_check(state_copy, i)):
                            legal_moves.append(i)
                        continue

                    kp = i

                if not in_check(state_copy, kp):
                    legal_moves.append(i)

        # Enables en passant
        if cm and cm[0] == 'P' and piece.id == 'P':
            m = int(cm[1])
            n = int(cm[2])
            q = int(cm[3])
            if y == q and abs(m - q) == 2 and abs(n - x) == 1:
                state_copy = deepcopy(state)
                state_copy[(m + q) // 2][n] = state_copy[y][x]
                state_copy[y][x] = None
                state_copy[y][n] = None
                if not in_check(state_copy, king_pos):
                    legal_moves.append(str((m + q) // 2) + str(n))

        return legal_moves

    # Highlights piece upon clicking and shows legal moves
    def move_preview(x, y):
        screen.blit(chessboard, [0, 0])
        board.display_state(screen, state, bc, sq_coord)

        # Displays green circles on squares where piece can legally move to
        surf1 = pygame.Surface(sq_coord, pygame.SRCALPHA)
        surf1.set_alpha(200)
        pygame.draw.circle(surf1, rgb_legal_move, half_sq_coord, 15)
        for i in legal_moves(x, y):
            screen.blit(surf1, bc[int(i[0])][int(i[1])])

        # Highlights square of king in green if player is not in check
        if (not in_check(state, king_pos())
                or king_pos() != str(y) + str(x)):
            surf = pygame.Surface(sq_coord)
            surf.fill(rgb_legal_move)
            surf.set_alpha(100)
            screen.blit(surf, bc[y][x])

        pygame.display.flip()

    # Displays the chess board and current position of pieces on screen
    def draw_board():
        screen.blit(chessboard, [0, 0])
        board.display_state(screen, state, bc, sq_coord)
        highlight_king()
        pygame.display.flip()

    # Checks if king is in check
    def in_check(state, king_pos):
        for i in state:
            for j in i:
                if j and j.team != turn and king_pos in j.moves(state):
                    return True
        return False

    # Returns all legal moves of player
    def all_legal_moves():
        all_legal_moves = []
        for i in state:
            for j in i:
                if j and j.team == turn:
                    for c in legal_moves(i.index(j), state.index(i)):
                        all_legal_moves.append(c)
        return len(all_legal_moves)

    # Highlights square of king in red if player is in check
    def highlight_king():
        kp = king_pos()
        if in_check(state, kp):
            a = int(kp[1])
            b = int(kp[0])
            surf2 = pygame.Surface(sq_coord)
            surf2.fill(rgb_check)
            surf2.set_alpha(80)
            screen.blit(surf2, bc[b][a])

    def current_count():
        counter = 0
        for i in state:
            for j in i:
                if j:
                    counter += 1
        return counter

    # FEN used to generate position
    def fen():
        raw_fen = 'r3k2r/p6p/8/B7/1pp1p3/3b4/P6P/R3K2R w KQkq - 0 1'

        info = {'turn': 1, 'castling': [], 'en_passant': None}

        fen = ''

        piece_count = 0
        flag = True

        for i in raw_fen:
            if i.isspace():
                fen += i
                flag = False
                continue
            elif i.isdigit() and flag:
                fen += int(i) * '0'
            elif i == '/':
                continue
            else:
                fen += i
                if flag:
                    piece_count += 1

        info['raw_fen'] = raw_fen

        info['fen'] = fen

        info['piece_count'] = piece_count

        info['move_count'] = int(fen[-fen[::-1].index(' '):])

        if fen[65] == 'b':
            info['turn'] = -1

        bk_index = fen.index('k')
        info['bk_pos'] = str(bk_index // 8) + str(bk_index % 8)
        wk_index = fen.index('K')
        info['wk_pos'] = str(wk_index // 8) + str(wk_index % 8)

        if fen[-5] == '3' or fen[-5] == '6':
            a = str(ord(fen[-6]) - 97)
            if fen[65] == 'b' and fen[-5] == '3':
                info['en_passant'] = 'P6' + a + '4' + a
            elif fen[65] == 'w' and fen[-5] == '6':
                info['en_passant'] = 'P1' + a + '3' + a

        castling_pos = {'K': '76', 'Q': '72', 'k': '06', 'q': '02'}
        i = 67
        while True:
            j = fen[i]
            if j == ' ' or j == '-':
                break
            elif j in castling_pos:
                info['castling'].append(castling_pos[j])
                i += 1
        # print(info)
        return info

    rgb_legal_move = (96, 145, 76)
    rgb_check = (236, 16, 18)

    scaling_factor = 5 / 44
    width = 880
    screen_size = [width] * 2
    sq_coord = [scaling_factor * x for x in screen_size]
    half_sq_coord = [0.5 * x for x in sq_coord]

    piece_selected = False
    flag = 0
    x = 0
    y = 0

    fen_info = fen()
    turn = fen_info['turn']
    cm = fen_info['en_passant']
    bk_pos = fen_info['bk_pos']
    wk_pos = fen_info['wk_pos']
    piece_count = fen_info['piece_count']
    move_count = fen_info['move_count']

    state = board.board(fen_info['fen'])

    screen = pygame.display.set_mode(screen_size)

    chessboard = board.chessboard_bg(width)
    bc = board.board_coordinates()
    draw_board()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if piece_selected:
                    a = board.grid(event.pos[0])
                    b = board.grid(event.pos[1])
                    if a is not None and b is not None:
                        c = str(b) + str(a)

                        # Moves piece if mouse clicks at legal move
                        if c in legal_moves(x, y):

                            # Removes captured pawn during en passant
                            if (state[y][x].id == 'P' and not state[b][a]
                                    and x != a):
                                state[y][int(cm[2])] = None

                            # Updates position of moved piece
                            state[b][a] = state[y][x]
                            state[b][a].row, state[b][a].col = b, a
                            state[y][x] = None

                            flag = 0

                            # Promotes pawn to queen if needed
                            if state[b][a].id == 'P' and not b % 7:
                                state[b][a] = pieces.Queen(turn, b, a)
                                flag += 1

                            # Updates position of king if it was moved
                            if state[b][a].id == 'K':
                                if turn == 1:
                                    wk_pos = c
                                else:
                                    bk_pos = c

                                # Updates position of rook if castled
                                if abs(x - a) == 2:
                                    if a == 6:
                                        state[b][5] = state[b][7]
                                        state[b][5].col = 5
                                        state[b][7] = None
                                        flag += 2
                                    else:
                                        state[b][3] = state[b][0]
                                        state[b][3].col = 3
                                        state[b][0] = None
                                        flag += 3

                            cm = state[b][a].id + str(y) + str(x) + c
                            if turn == 1:
                                dm = str(move_count) + '. '
                            else:
                                dm = ''

                            if cm[0] != 'P':
                                dm += cm[0]

                            cc = current_count()
                            if piece_count > cc:
                                if cm[0] != 'P':
                                    dm += 'x'
                                else:
                                    dm += chr(x + 97) + 'x'
                                piece_count = cc

                            dm += chr(int(c[1]) + 97) + str(8 - int(c[0]))

                            if flag == 1:
                                dm = dm[1:] + '=Q'

                            elif flag == 2:
                                dm = 'O-O'

                            elif flag == 3:
                                dm = 'O-O-O'

                            turn *= -1

                            if turn == 1:
                                move_count += 1

                            # Terminates game if stalemate or checkmate reached
                            if not all_legal_moves():
                                if turn == -1 and in_check(state, bk_pos):
                                    dm += '#'
                                    print(dm)
                                    print('White Wins')
                                elif turn == 1 and in_check(state, wk_pos):
                                    dm += '#'
                                    print(dm)
                                    print('Black Wins')
                                else:
                                    print(dm)
                                    print('Stalemate. Draw')
                                running = False

                            # Continues and updates game
                            else:
                                if (turn == -1 and in_check(state, bk_pos)
                                        or turn == 1
                                        and in_check(state, wk_pos)):
                                    dm += '+'
                                print(dm)
                                if hasattr(state[b][a], 'moved'):
                                    state[b][a].moved = True
                                draw_board()
                                piece_selected = False

                        # Displays legal moves of another selected piece
                        elif (state[b][a] and (a != x or b != y)
                                and state[b][a].team == turn):
                            x, y = a, b
                            move_preview(x, y)
                            piece_selected = True

                        # Deselects piece
                        else:
                            draw_board()
                            piece_selected = False

                # Selects piece
                else:
                    x = board.grid(event.pos[0])
                    y = board.grid(event.pos[1])
                    if (x is not None and y is not None
                            and state[y][x] and state[y][x].team == turn):
                        move_preview(x, y)
                        # print(all_legal_moves())
                        piece_selected = True

    # pygame.quit()
    # quit()


if __name__ == '__main__':
    main()
