import pygame

import board


def main():
    pygame.init()

    # Highlights piece upon clicking and shows legal moves
    def move_preview(x, y, state):
        screen.blit(chessboard, (0, 0))

        surf = pygame.Surface(sq_tuple)
        surf.fill(rgb_legal_move)
        surf.set_alpha(128)
        screen.blit(surf, nbc[y][x])

        board.display_board(screen, width, state, nbc)

        if state[y][x].legal_moves(state):
            s1 = pygame.Surface(sq_tuple, pygame.SRCALPHA)
            s1.set_alpha(175)
            pygame.draw.circle(
                s1, rgb_legal_move, half_sq_tuple, 15)
            for i in state[y][x].legal_moves(state):
                screen.blit(s1, nbc[int(i[0])][int(i[1])])

        pygame.display.flip()

    def draw_board():
        screen.blit(chessboard, (0, 0))
        board.display_board(screen, width, state, nbc)
        pygame.display.flip()

    rgb_legal_move = (96, 145, 76)

    sf = 5 / 44
    width = 880
    sq_width = sf * width
    sq_tuple = (sq_width, sq_width)
    half_sq_width = 0.5 * sq_width
    half_sq_tuple = (half_sq_width, half_sq_width)

    screen = pygame.display.set_mode((width, width))
    screen.fill((255, 255, 255))

    chessboard = board.chessboard_bg(width)
    state = board.board()
    nbc = board.board_coordinates()
    draw_board()

    piece_selected = False
    turn = 1
    x = 0
    y = 0

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
                        if str(b) + str(a) in state[y][x].legal_moves(state):
                            state[b][a] = state[y][x]
                            state[b][a].col, state[b][a].row = a, b
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
