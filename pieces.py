import pygame

pygame.init()

screen = pygame.display.set_mode([800, 800])


class Piece:
    def __init__(self, team, row, col):
        self.team = team
        self.row = row
        self.column = col

    def id(self, team):
        if team == 1:
            return 'W'
        return 'B'


class Pawn(Piece):
    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        filename = './Images/Sprites/' + self.id(team) + 'P' + '.png'
        self.image = pygame.image.load(filename)


x = Pawn(1, 2, 2)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    screen.blit(x.image, [0, 0])

    pygame.display.flip()

pygame.quit()
