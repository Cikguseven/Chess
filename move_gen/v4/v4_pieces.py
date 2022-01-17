from itertools import product


# Parent class for chess pieces
class Piece(object):
    def __init__(self, team, position):
        self.team = team
        self.pos = position

    @property
    def row(self):
        return self.pos // 8

    @property
    def col(self):
        return self.pos % 8

    def bishop_a_moves(self, state):
        moves = []

        for i in list(product([-1, 1], repeat=2)):
            x = self.col
            y = self.row
            while True:
                x += i[1]
                y += i[0]
                if 0 <= x <= 7 and 0 <= y <= 7:
                    new_pos = state.str(y * 8 + x)
                    if not new_pos or self.team != new_pos.team:
                        moves.append(str(y) + str(x))
                        if new_pos:
                            break
                    else:
                        break
                else:
                    break

        return moves

    def bishop_p_moves(self, state):
        moves = []
        enemy_king_pos = (state.black_king_pos if self.team == 1
                          else state.white_king_pos)

        for i in list(product([-1, 1], repeat=2)):
            x = self.col
            y = self.row
            while True:
                x += i[1]
                y += i[0]
                if 0 <= x <= 7 and 0 <= y <= 7:
                    new_pos = state.str(y * 8 + x)
                    if not new_pos or self.team != new_pos.team:
                        moves.append(str(y) + str(x))
                        if new_pos:
                            break
                    else:
                        break
                else:
                    break

        return moves

    def rook_a_moves(self, state):
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

    def rook_p_moves(self, state):
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

    def a_moves(self, state):
        moves = []
        pos = self.pos
        team = self.team
        y = self.row

        # Diagonal piece capture moves
        fl = pos - (9 * team)
        fl_row = fl // 8
        fl_sq = state.str(fl)
        if fl_sq and abs(fl_row - y) == 1 and team != fl_sq.team:
            moves.append(fl)

        fr = pos - (7 * team)
        fr_row = fr // 8
        fr_sq = state.str(fr)
        if fr_sq and abs(fr_row - y) == 1 and team != fr_sq.team:
            moves.append(fr)

        # Forward moves if square(s) ahead are empty
        fwd = pos - (8 * team)
        if not state.str(fwd):
            moves.append(fwd)
            fwd2 = fwd - (8 * team)
            if not ((y + team) % 7 or state.fwd2):
                moves.append(fwd2)

        # En passant
        ep = state.en_passant
        if ep[0] == 'p':
            os = int(ep[1:3])
            ns = int(ep[3:])

            if (y == ns // 8 and abs(os - ns) == 16
                    and abs(self.col - ns % 8) == 1):
                moves.append((os + ns) // 2)

        return moves

    def p_moves(self, state):
        moves = []

        # Guards diagonal squares
        fl = int(state.pos) - (9 * self.team)
        fl_row = fl // 8
        if abs(fl_row - self.row) == 1:
            moves.append(fl)

        fr = int(state.pos) - (7 * self.team)
        fr_row = fr // 8
        if abs(fr_row - self.row) == 1:
            moves.append(fr)

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

    def a_moves(self, state):
        return super().bishop_a_moves(state)

    def p_moves(self, state):
        return super().bishop_p_moves(state)


class Rook(Piece):

    id = 'R'

    def a_moves(self, state):
        return super().rook_a_moves(state)

    def p_moves(self, state):
        return super().rook_p_moves(state)


class Queen(Piece):

    id = 'Q'

    def a_moves(self, state):
        return [*super().bishop_a_moves(state),
                *super().rook_a_moves(state)]

    def p_moves(self, state):
        return [*super().bishop_p_moves(state),
                *super().rook_p_moves(state)]


class King(Piece):

    id = 'K'
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
        b = state[self.row]
        if self.row % 7 == 0 and self.col == 4:
            if not (b[1] or b[2] or b[3]) and b[0] and b[0].id == 'R':
                moves.append(str(self.row) + '2')
            if not (b[5] or b[6]) and b[7] and b[7].id == 'R':
                moves.append(str(self.row) + '6')
        return moves
