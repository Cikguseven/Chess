import pygame

import board

pygame.init()

width = 880

chessboard = chessboard_bg(width)

screen = pygame.display.set_mode([width, width])


for name in piece_names:
    filename = './Images/Sprites/' + name + '.png'
    images = pygame.image.load(filename)
    images = pygame.transform.scale(images, [100, 100])
    piece_images.append(images)

for j in range(2):
    for i in range(6):
        x, y = 100 * i, 100 * j
        coordinates.append([x, y])


class Piece:
    def __init__(self, team, type, image, value):
        self.team = team
        self.type = type
        self.image = image
        self.value = value


running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    screen.blit(chessboard, [0, 0])

    for a, b in zip(piece_images, coordinates):
        screen.blit(a, b)

    pygame.display.flip()

pygame.quit()
