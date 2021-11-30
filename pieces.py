import pygame

pygame.init()

# Scaling factor (sf) using piece to board ratio
sf = 5 / 44

# Width (& height) of square window
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
        self.moved = False

    def legalmove():
        pass


class Knight(Piece):
    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        filename = './Images/Sprites/' + self.id(team) + 'N' + '.png'
        self.image = pygame.image.load(filename)
        x = sf * width
        self.image = pygame.transform.scale(self.image, (x, x))

    def legalmove():
        pass


class Bishop(Piece):
    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        filename = './Images/Sprites/' + self.id(team) + 'B' + '.png'
        self.image = pygame.image.load(filename)
        x = sf * width
        self.image = pygame.transform.scale(self.image, (x, x))

    def legalmove():
        pass


class Rook(Piece):
    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        filename = './Images/Sprites/' + self.id(team) + 'R' + '.png'
        self.image = pygame.image.load(filename)
        x = sf * width
        self.image = pygame.transform.scale(self.image, (x, x))
        self.moved = False

    def legalmove():
        pass


class Queen(Piece):
    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        filename = './Images/Sprites/' + self.id(team) + 'Q' + '.png'
        self.image = pygame.image.load(filename)
        x = sf * width
        self.image = pygame.transform.scale(self.image, (x, x))

    def legalmove():
        pass


class King(Piece):
    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        filename = './Images/Sprites/' + self.id(team) + 'K' + '.png'
        self.image = pygame.image.load(filename)
        x = sf * width
        self.image = pygame.transform.scale(self.image, (x, x))
        self.moved = False

    def legalmove():
        pass
