import pygame

pygame.init()

screen_width = 800

screen_height = 800

screen = pygame.display.set_mode([screen_width, screen_height])

chessboard = pygame.image.load('./Images/Chessboard.png').convert()

chessboard = pygame.transform.scale(chessboard, [screen_width, screen_height])

piece_names = ['WP', 'WN', 'WB', 'WR', 'WQ', 'WK',
               'BP', 'BN', 'BB', 'BR', 'BQ', 'BK']

piece_images = []

coordinates = []

for name in piece_names:
    filename = './Images/Sprites/' + name + '.png'
    images = pygame.image.load(filename)
    images = pygame.transform.scale(images, [100, 100])
    piece_images.append(images)

for j in range(2):
    for i in range(6):
        x, y = 100 * i, 100 * j
        coordinates.append([x, y])

'''
class Pawn(pygame.sprite.Sprite):

    def __init__(self):

        super(Player, self).__init__()

        self.surf = pygame.Surface((75, 25))

        self.surf.fill((255, 255, 255))

        self.rect = self.surf.get_rect()
'''

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
