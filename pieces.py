import pygame

from itertools import product

pygame.init()

# Scaling factor (sf) using piece to board ratio
sf = 5 / 44

# Width (& height) of square window
width = 880

# Width (& height) of squares in chessboard
sq_width = sf * width

sq_tuple = (sq_width, sq_width)


class Piece(object):
    def __init__(self, team, row, col):
        self.team = team
        self.row = row
        self.col = col

        if team > 0:
            self.id = 'W'
        else:
            self.id = 'B'

        self.filename = './Images/Sprites/' + self.id

    def bishop_moves(self, sp):
        moves = []
        for i in list(product(range(-1, 2, 2), repeat=2)):
            x = self.col
            y = self.row
            while True:
                y += i[0]
                x += i[1]
                if 0 <= y <= 7 and 0 <= x <= 7:
                    c = sp[y][x]
                    if not c or c.team == -self.team:
                        moves.append(str(y) + str(x))
                        if c and c.team == -self.team:
                            break
                    else:
                        break
                else:
                    break
        return moves

    def rook_moves(self, sp):
        moves = []
        for i in list(product(range(-1, 2), repeat=2)):
            if abs(sum(i)) == 1:
                x = self.col
                y = self.row
                while True:
                    y += i[0]
                    x += i[1]
                    if 0 <= y <= 7 and 0 <= x <= 7:
                        c = sp[y][x]
                        if not c or c.team == -self.team:
                            moves.append(str(y) + str(x))
                            if c and c.team == -self.team:
                                break
                        else:
                            break
                    else:
                        break
        return moves


class Pawn(Piece):
    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        self.image = pygame.image.load(self.filename + 'P' + '.png')
        self.image = pygame.transform.scale(self.image, sq_tuple)
        self.moved = False

    def legal_moves(self, sp):
        moves = []
        x = self.col
        y = self.row
        if self.team == 1:
            if x != 0:
                fl = sp[y - 1][x - 1]
                if fl and fl.team == -1:
                    moves.append(str(y - 1) + str(x - 1))
            if x != 7:
                fr = sp[y - 1][x + 1]
                if fr and fr.team == -1:
                    moves.append(str(y - 1) + str(x + 1))
            if y:
                if not sp[y - 1][x]:
                    moves.append(str(y - 1) + str(x))
                    if not self.moved and not sp[y - 2][x]:
                        moves.append(str(y - 2) + str(x))
            else:
                return None
        else:
            if x != 0:
                bl = sp[y + 1][x - 1]
                if bl and bl.team == 1:
                    moves.append(str(y + 1) + str(x - 1))
            if x != 7:
                br = sp[y + 1][x + 1]
                if br and br.team == 1:
                    moves.append(str(y + 1) + str(x + 1))
            if y < 7:
                if not sp[y + 1][x]:
                    moves.append(str(y + 1) + str(x))
                    if not self.moved and not sp[y + 2][x]:
                        moves.append(str(y + 2) + str(x))
            else:
                return None
        return moves


class Knight(Piece):
    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        self.image = pygame.image.load(self.filename + 'N' + '.png')
        self.image = pygame.transform.scale(self.image, sq_tuple)

    def legal_moves(self, sp):
        moves = []
        for i in list(product(range(-2, 3), repeat=2)):
            if abs(i[0]) + abs(i[1]) == 3:
                x = self.col + i[0]
                y = self.row + i[1]
                if 0 <= x <= 7 and 0 <= y <= 7:
                    a = sp[y][x]
                    if not a or a.team == -self.team:
                        moves.append(str(y) + str(x))
        return moves


class Bishop(Piece):
    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        self.image = pygame.image.load(self.filename + 'B' + '.png')
        self.image = pygame.transform.scale(self.image, sq_tuple)

    def legal_moves(self, sp):
        return super().bishop_moves(sp)


class Rook(Piece):
    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        self.image = pygame.image.load(self.filename + 'R' + '.png')
        self.image = pygame.transform.scale(self.image, sq_tuple)
        self.moved = False

    def legal_moves(self, sp):
        return super().rook_moves(sp)


class Queen(Piece):
    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        self.image = pygame.image.load(self.filename + 'Q' + '.png')
        self.image = pygame.transform.scale(self.image, sq_tuple)

    def legal_moves(self, sp):
        bishop_moves = super().bishop_moves(sp)
        rook_moves = super().rook_moves(sp)
        return [*bishop_moves, *rook_moves]


class King(Piece):
    def __init__(self, team, row, col):
        super().__init__(team, row, col)
        self.image = pygame.image.load(self.filename + 'K' + '.png')
        self.image = pygame.transform.scale(self.image, sq_tuple)
        self.moved = False

    def legal_moves(self, sp):
        king_moves = list(product(range(-1, 2), repeat=2))
        king_moves.remove((0, 0))
        moves = []
        for i in king_moves:
            x = self.col + i[0]
            y = self.row + i[1]
            if 0 <= x <= 7 and 0 <= y <= 7:
                a = sp[y][x]
                if a and abs(self.team - a.team) != 3:
                    continue
                moves.append(str(y) + str(x))
        return moves
