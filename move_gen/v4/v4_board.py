class Board(object):
    def __init__(self, fen):

        print('position fen ' + fen)

        piece_id = {'p': Pawn, 'n': Knight, 'b': Bishop,
                    'r': Rook, 'q': Queen, 'k': King}

        fen = fen.replace('/', '')

        for i in range(64):
            setattr(self, str(i), None)

        self.white_piece_pos = ''
        self.black_piece_pos = ''

        counter = 0

        for i in fen:
            if counter < 64:

                if i.isdigit():
                    counter += int(i)

                else:
                    j = str(counter)

                    if i.islower():
                        setattr(self, j, piece_id[i](1, counter))
                        self.black_piece_pos += lzero(counter) + i
                        if i == 'k':
                            setattr(self, 'black_king_pos', counter)

                    else:
                        setattr(self, j, piece_id[i.lower()](-1, counter))
                        self.white_piece_pos += lzero(counter) + i
                        if i == 'K':
                            setattr(self, 'white_king_pos', counter)

                    counter += 1

            else:
                break

        self.turn = -1 if fen[fen.find(' ') + 1] == 'b' else 1

        self.en_passant = '0'

        if fen[-5] in {'3', '6'}:
            col = ord(fen[-6]) - 97

            if self.turn == -1 and fen[-5] == '3':
                self.en_passant = 'p' + str(48 + col) + str(32 + col)

            elif self.turn == 1 and fen[-5] == '6':
                self.en_passant = 'p' + lzero(8 + col) + str(24 + col)

        castling = ['K', 'Q', 'k', 'q']

        for i in castling:
            setattr(self, i, False)

        i = fen.find(' ') + 3

        while True:
            if fen[i] in {' ', '-'}:
                break

            else:
                setattr(self, fen[i], True)
                i += 1
