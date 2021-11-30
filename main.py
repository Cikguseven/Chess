import pygame

import board


def main():
    pygame.init()

    rgb_legal_move = (96, 145, 76)

    sf = 5 / 44
    width = 880
    square_width = sf * width
    square_tuple = (square_width, square_width)

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
                x = board.row(event.pos[0])
                y = board.row(event.pos[1])
                if x is not None and y is not None and sp[y][x]:
                    surf = pygame.Surface(square_tuple)
                    surf.fill(rgb_legal_move)
                    surf.set_alpha(128)
                    z = nbc[y][x]
                    screen.blit(chessboard, (0, 0))
                    screen.blit(surf, z)
                    board.display_board(screen, width, sp, nbc)
                    pygame.display.flip()
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
