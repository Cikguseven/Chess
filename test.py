def an(pos):
    return chr(pos % 8 + 97) + str(8 - pos // 8)


class Piece(object):
    def __init__(self, team, position):
        self.team = team
        self.pos = position


class Pawn(Piece):
    id = 'P'


class Knight(Piece):
    id = 'N'


class Bishop(Piece):
    id = 'B'


class Rook(Piece):
    id = 'R'


class Queen(Piece):
    id = 'Q'


class King(Piece):
    id = 'K'


class Board(object):
    def __init__(self, fen):

        piece_id = {'p': Pawn, 'n': Knight, 'b': Bishop,
                    'r': Rook, 'q': Queen, 'k': King}

        fen = fen.replace('/', '')

        counter = 0

        for i in fen:
            if counter < 64:
                j = an(counter)
                print(j)

                if i.isdigit():
                    counter += int(i)

                else:
                    if i.islower():
                        setattr(self, j, piece_id[i](1, counter))

                    else:
                        setattr(self, j, piece_id[i.lower()](1, counter))

                    counter += 1

            else:
                break


x = Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

print(x.__dict__)
