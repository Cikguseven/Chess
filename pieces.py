import pygame

from itertools import product

pygame.init()


class Piece(object):
    def __init__(self, team, row, column):
        self.team = team
        self.row = row
        self.col = column

    def filename(self):
        if self.team > 0:
            return './Images/Sprites/W'
        else:
            return './Images/Sprites/B'

    def bishop_moves(self, state):
        moves = []
        for i in list(product(range(-1, 2, 2), repeat=2)):
            x = self.col
            y = self.row
            while True:
                y += i[0]
                x += i[1]
                if 0 <= y <= 7 and 0 <= x <= 7:
                    a = state[y][x]
                    if not a or self.team != a.team:
                        moves.append(str(y) + str(x))
                        if a and self.team != a.team:
                            break
                    else:
                        break
                else:
                    break
        return moves

    def rook_moves(self, state):
        moves = []
        for i in list(product(range(-1, 2), repeat=2)):
            if abs(sum(i)) == 1:
                x = self.col
                y = self.row
                while True:
                    y += i[0]
                    x += i[1]
                    if 0 <= y <= 7 and 0 <= x <= 7:
                        a = state[y][x]
                        if not a or self.team != a.team:
                            moves.append(str(y) + str(x))
                            if a and self.team != a.team:
                                break
                        else:
                            break
                    else:
                        break
        return moves


class Pawn(Piece):

    id = 'P'

    def moves(self, state):
        moves = []
        x = self.col
        y = self.row
        z = self.team
        if x != 0:
            a = state[y - z][x - 1]
            if a and z != a.team:
                moves.append(str(y - z) + str(x - 1))
        if x != 7:
            b = state[y - z][x + 1]
            if b and z != b.team:
                moves.append(str(y - z) + str(x + 1))
        if not state[y - z][x]:
            moves.append(str(y - z) + str(x))
            if (y + z) % 7 == 0 and not state[y - (2 * z)][x]:
                moves.append(str(y - (2 * z)) + str(x))
        return moves


class Knight(Piece):

    id = 'N'

    def moves(self, state):
        moves = []
        for i in list(product(range(-2, 3), repeat=2)):
            if abs(i[0]) + abs(i[1]) == 3:
                x = self.col + i[0]
                y = self.row + i[1]
                if 0 <= x <= 7 and 0 <= y <= 7:
                    a = state[y][x]
                    if not a or self.team != a.team:
                        moves.append(str(y) + str(x))
        return moves


class Bishop(Piece):

    id = 'B'

    def moves(self, state):
        return super().bishop_moves(state)


class Rook(Piece):

    id = 'R'
    moved = False

    def moves(self, state):
        return super().rook_moves(state)


class Queen(Piece):

    id = 'Q'

    def moves(self, state):
        bishop_moves = super().bishop_moves(state)
        rook_moves = super().rook_moves(state)
        return [*bishop_moves, *rook_moves]


class King(Piece):

    id = 'K'
    moved = False
    immune = True

    def moves(self, state):
        moves = []
        king_moves = list(product(range(-1, 2), repeat=2))
        king_moves.remove((0, 0))
        for i in king_moves:
            x = self.col + i[0]
            y = self.row + i[1]
            if 0 <= x <= 7 and 0 <= y <= 7:
                a = state[y][x]
                if not a or self.team != a.team:
                    moves.append(str(y) + str(x))
        if not self.moved:
            b = state[self.row]
            if not (b[1] or b[2] or b[3]):
                lr = b[0]
                if lr and lr.id == 'R' and not lr.moved:
                    moves.append(str(self.row) + '2')
            if not (b[5] or b[6]):
                rr = b[7]
                if rr and rr.id == 'R' and not rr.moved:
                    moves.append(str(self.row) + '6')
        return moves
