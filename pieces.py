import pygame

pygame.init()

# Scaling factor (sf) using piece to board ratio
sf = 5 / 44

# Width (& height) of square window
width = 880

# Width (& height) of squares in chessboard
sq_width = sf * width

sq_tuple = (sq_width, sq_width)

half_sq_width = 0.5 * sq_width

half_sq_tuple = (half_sq_width, half_sq_width)

rgb_legal_move = (96, 145, 76)


class Piece:
    def __init__(self, team, row, col):
        self.team = team
        self.row = row
        self.col = col

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
        self.image = pygame.transform.scale(self.image, sq_tuple)
        self.moved = False

    def legal_moves(self, nbc):
        moves = []
        if self.team == 1:
            if not self.moved:
                moves.append(str(self.row - 1) + str(self.col))
                moves.append(str(self.row - 2) + str(self.col))
            elif self.row:
                moves.append(str(self.row - 1) + str(self.col))
            else:
                return None
        else:
            if not self.moved:
                moves.append(str(self.row + 1) + str(self.col))
                moves.append(str(self.row + 2) + str(self.col))
            elif self.row != 7:
                moves.append(str(self.row + 1) + str(self.col))
            else:
                return None
        return moves


class Knight(Piece):
    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        filename = './Images/Sprites/' + self.id(team) + 'N' + '.png'
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, sq_tuple)

    def legal_moves(self, nbc):
        pass


class Bishop(Piece):
    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        filename = './Images/Sprites/' + self.id(team) + 'B' + '.png'
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, sq_tuple)

    def legal_moves(self, nbc):
        pass


class Rook(Piece):
    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        filename = './Images/Sprites/' + self.id(team) + 'R' + '.png'
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, sq_tuple)
        self.moved = False

    def legal_moves(self, nbc):
        pass


class Queen(Piece):
    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        filename = './Images/Sprites/' + self.id(team) + 'Q' + '.png'
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, sq_tuple)

    def legal_moves(self, nbc):
        pass


class King(Piece):
    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        filename = './Images/Sprites/' + self.id(team) + 'K' + '.png'
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, sq_tuple)
        self.moved = False

    def legal_moves(self, nbc):
        pass
