import pygame

import board

pygame.init()

width = 880

screen = pygame.display.set_mode([width, width])

chessboard = board.chessboard_bg(width)

sp = board.board()

nbc = board.board_coordinates()

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    screen.blit(chessboard, [0, 0])

    board.display_board(screen, width, sp, nbc)

    pygame.display.flip()

pygame.quit()
