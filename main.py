import pygame

import board

from copy import deepcopy


def main():
    pygame.init()

    # Checks if move is legal (does not result in check)
    def move_checker(x, y, state, turn, wk_pos, bk_pos):
        checked_moves = []
        a = state[y][x].moves(state)
        for i in a:
            state_copy = deepcopy(state)
            w = wk_pos
            b = bk_pos
            j = int(i[0])
            k = int(i[1])
            if not hasattr(state_copy[j][k], 'immune'):
                state_copy[j][k] = state_copy[y][x]
                state_copy[y][x] = None
                if hasattr(state_copy[j][k], 'immune'):
                    if turn == 1:
                        w = str(j) + str(k)
                    else:
                        b = str(j) + str(k)
                if not in_check(turn, state_copy, w, b):
                    checked_moves.append(str(j) + str(k))
        return checked_moves

    # Highlights piece upon clicking and shows legal moves
    def move_preview(x, y, state):
        screen.blit(chessboard, [0, 0])

        surf = pygame.Surface(sq_coord)
        surf.fill(rgb_legal_move)
        surf.set_alpha(128)
        screen.blit(surf, nbc[y][x])

        board.display_state(screen, state, nbc, sq_coord)

        move_checker(x, y, state, turn, wk_pos, bk_pos)

        surf1 = pygame.Surface(sq_coord, pygame.SRCALPHA)
        surf1.set_alpha(175)
        pygame.draw.circle(
            surf1, rgb_legal_move, half_sq_coord, 15)

        a = move_checker(x, y, state, turn, wk_pos, bk_pos)

        if a:
            for i in a:
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
                    # print('in check')
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
    # Default '04'
    bk_pos = '04'
    # Default '74'
    wk_pos = '74'

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
                        if c in state[y][x].moves(state):
                            if not hasattr(state[b][a], 'immune'):
                                state[b][a] = state[y][x]
                                state[b][a].col, state[b][a].row = a, b
                                if hasattr(state[b][a], 'moved'):
                                    state[b][a].moved = True
                                    if hasattr(state[b][a], 'immune'):
                                        if turn == 1:
                                            wk_pos = c
                                        else:
                                            bk_pos = c
                                state[y][x] = None
                                draw_board()
                                piece_selected = False
                                turn *= -1
                        elif (state[b][a] and (a != x or b != y)
                                and state[b][a].team == turn):
                            x = a
                            y = b
                            move_preview(x, y, state)
                            piece_selected = True
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
