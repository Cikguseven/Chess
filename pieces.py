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
                    c = state[y][x]
                    if not c or self.team != c.team:
                        moves.append(str(y) + str(x))
                        if c and self.team != c.team:
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
                        c = state[y][x]
                        if not c or self.team != c.team:
                            moves.append(str(y) + str(x))
                            if c and self.team != c.team:
                                break
                        else:
                            break
                    else:
                        break
        return moves


class Pawn(Piece):

    id = 'P'
    moved = False

    def moves(self, state):
        moves = []
        x = self.col
        y = self.row
        if self.team == 1:
            if x != 0:
                fl = state[y - 1][x - 1]
                if fl and fl.team == -1:
                    moves.append(str(y - 1) + str(x - 1))
            if x != 7:
                fr = state[y - 1][x + 1]
                if fr and fr.team == -1:
                    moves.append(str(y - 1) + str(x + 1))
            if y:
                if not state[y - 1][x]:
                    moves.append(str(y - 1) + str(x))
                    if not self.moved and not state[y - 2][x]:
                        moves.append(str(y - 2) + str(x))
        else:
            if x != 0:
                bl = state[y + 1][x - 1]
                if bl and bl.team == 1:
                    moves.append(str(y + 1) + str(x - 1))
            if x != 7:
                br = state[y + 1][x + 1]
                if br and br.team == 1:
                    moves.append(str(y + 1) + str(x + 1))
            if y < 7:
                if not state[y + 1][x]:
                    moves.append(str(y + 1) + str(x))
                    if not self.moved and not state[y + 2][x]:
                        moves.append(str(y + 2) + str(x))
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
                if lr and type(lr).__name__ == 'Rook' and not lr.moved:
                    moves.append(str(self.row) + '2')
            if not (b[5] or b[6]):
                rr = b[7]
                if rr and type(rr).__name__ == 'Rook' and not rr.moved:
                    moves.append(str(self.row) + '6')
        return moves
