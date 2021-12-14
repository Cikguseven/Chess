import time

start = time.time()

from pprint import pprint
from copy import deepcopy
from itertools import product


class Piece(object):
    def __init__(self, team, row, column):
        self.team = team
        self.row = row
        self.col = column

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


# Initialises position from Forsyth–Edwards Notation (FEN)
def board(fen):

    board = [[fen[(8 * i) + j] for j in range(8)] for i in range(8)]

    piece_id = {'p': Pawn, 'n': Knight, 'b': Bishop,
                'r': Rook, 'q': Queen, 'k': King}

    for i in board:
        for j in i:
            a = board.index(i)
            b = i.index(j)
            if not j.isdigit():
                if j.isupper():
                    team = 1
                else:
                    team = -1
                board[a][b] = piece_id[j.lower()](
                    team, board.index(i), i.index(j))
            else:
                board[a][b] = None

    return board


def an(move, id):
    '''
    if id == 'P':
        id = ''
    return id + chr(int(move[1]) + 97) + str(8 - int(move[0]))
    '''
    return chr(int(move[1]) + 97) + str(8 - int(move[0]))


# Checks if move is legal (does not result in check)
def legal_moves(piece, wk_pos, bk_pos, state, cm, castling, turn):
    legal_moves = []
    y = piece.row
    x = piece.col

    for i in piece.moves(state):
        if turn == 1:
            kp = wk_pos
        else:
            kp = bk_pos
        state_copy = deepcopy(state)
        j, k = int(i[0]), int(i[1])
        # Removes king capturing moves
        if not hasattr(state_copy[j][k], 'immune'):

            if (state_copy[y][x].id == 'P'
                    and not state_copy[j][k] and k != x):
                state_copy[y][int(cm[2])] = None

            # Test if new position results in check
            state_copy[j][k] = state_copy[y][x]
            state_copy[y][x] = None

            if state_copy[j][k].id == 'K':

                # Enables castling
                if abs(x - k) == 2:
                    if (i in castling and not in_check(state, kp, turn)
                        and str(y) + str((x + k) // 2) in legal_moves
                            and not in_check(state_copy, i, turn)):
                        legal_moves.append(i)
                    continue

                kp = i

            if not in_check(state_copy, kp, turn):
                legal_moves.append(i)

    # Enables en passant
    if cm and cm[0] == 'P' and piece.id == 'P':
        if turn == 1:
            kp = wk_pos
        else:
            kp = bk_pos
        m = int(cm[1])
        n = int(cm[2])
        q = int(cm[3])
        if y == q and abs(m - q) == 2 and abs(n - x) == 1:
            state_copy = deepcopy(state)
            state_copy[(m + q) // 2][n] = state_copy[y][x]
            state_copy[y][x] = None
            state_copy[y][n] = None
            if not in_check(state_copy, kp, turn):
                legal_moves.append(str((m + q) // 2) + str(n))

    return legal_moves


# Checks if king is in check
def in_check(state, king_pos, turn):
    for i in state:
        for j in i:
            if j and j.team != turn and king_pos in j.moves(state):
                return True
    return False


# FEN used to generate position
def fen(raw_fen):
    print('position fen ' + raw_fen)

    info = {'turn': 1, 'castling': [], 'en_passant': None}

    fen = ''

    flag = True

    for i in raw_fen:
        if i.isspace():
            fen += i
            flag = False
            continue
        elif i.isdigit() and flag:
            fen += int(i) * '0'
        elif i == '/':
            continue
        else:
            fen += i

    info['fen'] = fen

    if fen[65] == 'b':
        info['turn'] = -1

    bk_index = fen.index('k')
    info['bk_pos'] = str(bk_index // 8) + str(bk_index % 8)
    wk_index = fen.index('K')
    info['wk_pos'] = str(wk_index // 8) + str(wk_index % 8)

    if fen[-5] == '3' or fen[-5] == '6':
        a = str(ord(fen[-6]) - 97)
        if fen[65] == 'b' and fen[-5] == '3':
            info['en_passant'] = 'P6' + a + '4' + a
        elif fen[65] == 'w' and fen[-5] == '6':
            info['en_passant'] = 'P1' + a + '3' + a

    castling_pos = {'K': '76', 'Q': '72', 'k': '06', 'q': '02'}
    i = 67
    while True:
        j = fen[i]
        if j == ' ' or j == '-':
            break
        elif j in castling_pos:
            info['castling'].append(castling_pos[j])
            i += 1
    pprint(info)
    return info

# Generates legal moves to chosen depth, output is similar to Stockfish


def move_gen(depth, dc, state, turn, wk_pos, bk_pos, cm, castling):
    counter = 0
    if depth == 0:
        return 1
    else:
        for i in state:
            for j in i:
                if j and j.team == turn:
                    k = legal_moves(j, wk_pos, bk_pos, state,
                                    cm, castling, turn)
                    n = j.id
                    if k:
                        for m in k:
                            e = cm
                            f = deepcopy(castling)
                            g = wk_pos
                            h = bk_pos
                            sc = deepcopy(state)
                            a = int(m[1])
                            b = int(m[0])
                            c = i.index(j)
                            d = state.index(i)
                            if (sc[d][c].id == 'P' and not sc[b][a]
                                    and c != a):
                                sc[d][int(cm[2])] = None
                            sc[b][a] = sc[d][c]
                            sc[b][a].row, sc[b][a].col = b, a
                            sc[d][c] = None
                            rook_pos = {'77': '76', '70': '72',
                                        '07': '06', '00': '02'}
                            z = [m, str(d) + str(c)]
                            for pos in z:
                                if pos in rook_pos and rook_pos[pos] in f:
                                    f.remove(rook_pos[pos])
                            if n == 'K':
                                if turn == 1:
                                    wcr = ['72', '76']
                                    for cr in wcr:
                                        if g == '74' and cr in f:
                                            f.remove(cr)
                                    g = m
                                else:
                                    bcr = ['02', '06']
                                    for cr in bcr:
                                        if g == '04' and cr in f:
                                            f.remove(cr)
                                    h = m
                                if abs(c - a) == 2:
                                    if a == 6:
                                        sc[b][5] = sc[b][7]
                                        sc[b][5].col = 5
                                        sc[b][7] = None
                                    else:
                                        sc[b][3] = sc[b][0]
                                        sc[b][3].col = 3
                                        sc[b][0] = None
                            if n == 'P' and not b % 7:
                                promotion = [Queen, Bishop, Rook, Knight]
                                for p in promotion:
                                    z = str(p)[17].lower()
                                    if z == 'k':
                                        z = 'n'
                                    sd = deepcopy(sc)
                                    sd[b][a] = p(turn, b, a)
                                    e = sd[b][a].id + \
                                        str(d) + str(c) + str(b) + str(a)
                                    x = move_gen(depth - 1, dc, sd, -turn,
                                                 g, h, e, f)
                                    if depth == dc:
                                        print(f'{an(str(d) + str(c), n)}{an(m, n)}{z}: {x}')
                                    counter += x
                            else:
                                e = sc[b][a].id + \
                                    str(d) + str(c) + str(b) + str(a)
                                x = move_gen(depth - 1, dc, sc, -turn,
                                             g, h, e, f)
                                if depth == dc:
                                    print(f'{an(str(d) + str(c), n)}{an(m, n)}: {x}')
                                counter += x
        return counter


# Input FEN of position
test = '8/6kp/7R/6Pp/r4P2/8/5K2/8 w - - 9 59'

fen_info = fen(test)
turn = fen_info['turn']
cm = fen_info['en_passant']
bk_pos = fen_info['bk_pos']
wk_pos = fen_info['wk_pos']
castling = fen_info['castling']

state = board(fen_info['fen'])

print(move_gen(4, 4, state, turn, wk_pos, bk_pos, cm, castling))

end = time.time()

print(end - start)
