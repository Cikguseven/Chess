import pygame

import board

from copy import deepcopy


def main():
    pygame.init()

    # Checks if move is legal (does not result in check)
    def legal_moves(x, y, state, turn, wk_pos, bk_pos):
        legal_moves = []
        a = state[y][x].moves(state)
        for i in a:
            state_copy = deepcopy(state)
            w, b = wk_pos, bk_pos
            j, k = int(i[0]), int(i[1])
            if not hasattr(state_copy[j][k], 'immune'):
                state_copy[j][k] = state_copy[y][x]
                state_copy[y][x] = None
                if hasattr(state_copy[j][k], 'immune'):
                    if turn == 1:
                        w = str(j) + str(k)
                    else:
                        b = str(j) + str(k)
                    if abs(x - k) == 2:
                        state_copy1 = deepcopy(state)
                        state_copy1[j][(x + k) // 2] = state_copy1[j][x]
                        state_copy1[j][x] = None
                        if (turn == 1
                            and (not (in_check(turn, state_copy1,
                                               str(y) + str((x + k) // 2), b)
                                      or in_check(turn, state_copy, w, b)))):
                            legal_moves.append(w)
                        elif (turn == -1
                              and not (in_check(turn, state_copy1, w,
                                                str(y) + str((x + k) // 2))
                                       or in_check(turn, state_copy, w, b))):
                            legal_moves.append(b)
                        continue
                if not in_check(turn, state_copy, w, b):
                    legal_moves.append(str(j) + str(k))
        return legal_moves

    # Highlights piece upon clicking and shows legal moves
    def move_preview(x, y, state):
        screen.blit(chessboard, [0, 0])

        surf = pygame.Surface(sq_coord)
        surf.fill(rgb_legal_move)
        surf.set_alpha(128)
        screen.blit(surf, nbc[y][x])

        board.display_state(screen, state, nbc, sq_coord)

        surf1 = pygame.Surface(sq_coord, pygame.SRCALPHA)
        surf1.set_alpha(175)
        pygame.draw.circle(surf1, rgb_legal_move, half_sq_coord, 15)

        for i in legal_moves(x, y, state, turn, wk_pos, bk_pos):
            screen.blit(surf1, nbc[int(i[0])][int(i[1])])

        pygame.display.flip()

    # Displays the chess board and current position of pieces on screen
    def draw_board():
        screen.blit(chessboard, [0, 0])
        board.display_state(screen, state, nbc, sq_coord)
        pygame.display.flip()

    def in_check(turn, state, wk_pos, bk_pos):
        if turn == 1:
            k = wk_pos
        else:
            k = bk_pos
        for i in state:
            for j in i:
                if j and j.team != turn and k in j.moves(state):
                    return True
        return False

    def checkmate(state, turn, wk_pos, bk_pos):
        valid_moves = []
        for i in state:
            for j in i:
                if j and j.team == turn:
                    a = i.index(j)
                    b = state.index(i)
                    for k in legal_moves(a, b, state, turn, wk_pos, bk_pos):
                        valid_moves.append(k)
        if not valid_moves:
            return True
        return False

    rgb_legal_move = (96, 145, 76)
    rgb_check = (236, 16, 18)

    sf = 5 / 44
    width = 880
    screen_size = [width] * 2
    sq_coord = [sf * x for x in screen_size]
    half_sq_coord = [0.5 * x for x in sq_coord]

    screen = pygame.display.set_mode(screen_size)

    chessboard = board.chessboard_bg(width)
    nbc = board.board_coordinates()
    state = board.board()
    draw_board()

    piece_selected = False
    turn = 1
    bk_pos, wk_pos = '04', '74'

    running = True

    flag = True

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
                        # Moves piece if mouse clicks legal position
                        if c in legal_moves(x, y, state, turn, wk_pos, bk_pos):
                            state[b][a] = state[y][x]
                            state[b][a].row, state[b][a].col = b, a
                            state[y][x] = None
                            if (hasattr(state[b][a], 'immune')
                                    and abs(x - a) == 2):
                                if a == 6:
                                    state[b][5] = state[b][7]
                                    state[b][5].col = 5
                                    state[b][7] = None
                                else:
                                    state[b][3] = state[b][0]
                                    state[b][3].col = 3
                                    state[b][0] = None
                            turn *= -1
                            if checkmate(state, turn, wk_pos, bk_pos):
                                if turn == -1:
                                    print('white wins')
                                else:
                                    print('black wins')
                                running = False
                            else:
                                if hasattr(state[b][a], 'moved'):
                                    state[b][a].moved = True
                                    if hasattr(state[b][a], 'immune'):
                                        if turn == -1:
                                            wk_pos = c
                                        else:
                                            bk_pos = c
                                draw_board()
                                piece_selected = False
                        # Displays legal moves of another selected piece
                        elif (state[b][a] and (a != x or b != y)
                                and state[b][a].team == turn):
                            x, y = a, b
                            move_preview(x, y, state)
                            piece_selected = True
                        # Deselects piece
                        else:
                            draw_board()
                            piece_selected = False
                else:
                    x = board.grid(event.pos[0])
                    y = board.grid(event.pos[1])
                    if (x is not None and y is not None
                            and state[y][x] and state[y][x].team == turn):
                        move_preview(x, y, state)
                        piece_selected = True



    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
