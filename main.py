import pygame

import board


def main():
    pygame.init()

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
    sp = board.board()
    nbc = board.board_coordinates()

    screen.blit(chessboard, (0, 0))
    board.display_board(screen, width, sp, nbc)
    pygame.display.flip()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Highlights piece upon clicking
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = board.grid_pos(event.pos[0])
                y = board.grid_pos(event.pos[1])
                if x is not None and y is not None and sp[y][x]:
                    screen.blit(chessboard, (0, 0))
                    surf = pygame.Surface(sq_tuple)
                    surf.fill(rgb_legal_move)
                    surf.set_alpha(128)
                    screen.blit(surf, nbc[y][x])
                    z = sp[y][x].legal_moves(nbc)
                    if z:
                        s1 = pygame.Surface(sq_tuple, pygame.SRCALPHA)
                        s1.set_alpha(200)
                        pygame.draw.circle(
                            s1, rgb_legal_move, half_sq_tuple, 15)
                        for i in z:
                            screen.blit(s1, nbc[int(i[0])][int(i[1])])
                    board.display_board(screen, width, sp, nbc)
                    pygame.display.flip()

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
