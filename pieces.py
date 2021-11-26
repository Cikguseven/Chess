import pygame

pygame.init()

sf = 5 / 44

width = 880


class Piece:
    def __init__(self, team, row, col):
        self.team = team
        self.row = row
        self.column = col

    def id(self, team):
        if team == 1:
            return 'W'
        return 'B'

    def image(self, team, piece):
        if team == 1:
            return './Images/Sprites/' + 'W' + self.piece


class Pawn(Piece):
    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        filename = './Images/Sprites/' + self.id(team) + 'P' + '.png'
        self.image = pygame.image.load(filename)
        x = sf * width
        self.image = pygame.transform.scale(self.image, (x, x))

    def legalmove():
        pass
