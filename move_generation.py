import board

from copy import deepcopy


def main():
    def king_pos():
        if turn == 1:
            return wk_pos
        else:
            return bk_pos

    def move_gen():
        '''
        if depth == 0:
            return 1
        '''
        moves = []
        for i in state:
            for j in i:
                if j and j.team == turn:
                    k = legal_moves(j)
                    for m in k:
                        moves.append(m)
        print(moves)
        print(len(moves))

    # Checks if move is legal (does not result in check)
    def legal_moves(piece):
        legal_moves = []
        kp = king_pos()
        castling = fen_info['castling']
        y = piece.row
        x = piece.col

        for i in piece.moves(state):
            state_copy = deepcopy(state)
            j, k = int(i[0]), int(i[1])
            # Removes king capturing moves
            if not hasattr(state_copy[j][k], 'immune'):

                # Test if new position results in check
                state_copy[j][k] = state_copy[y][x]
                state_copy[y][x] = None
                if state_copy[j][k].id == 'K':

                    # Enables castling
                    if abs(x - k) == 2:
                        if (i in castling and not in_check(state, kp)
                            and str(y) + str((x + k) // 2) in legal_moves
                                and not in_check(state_copy, i)):
                            legal_moves.append(i)
                        continue

                    kp = i

                if not in_check(state_copy, kp):
                    legal_moves.append(i)

        # Enables en passant
        if cm and cm[0] == 'P' and piece.id == 'P':
            m = int(cm[1])
            n = int(cm[2])
            q = int(cm[3])
            if y == q and abs(m - q) == 2 and abs(n - x) == 1:
                state_copy = deepcopy(state)
                state_copy[(m + q) // 2][n] = state_copy[y][x]
                state_copy[y][x] = None
                state_copy[y][n] = None
                if not in_check(state_copy, king_pos):
                    legal_moves.append(str((m + q) // 2) + str(n))

        return legal_moves

    # Checks if king is in check
    def in_check(state, king_pos):
        for i in state:
            for j in i:
                if j and j.team != turn and king_pos in j.moves(state):
                    return True
        return False

    # Returns all legal moves of player
    def all_legal_moves():
        all_legal_moves = []
        for i in state:
            for j in i:
                if j and j.team == turn:
                    for c in legal_moves(i.index(j), state.index(i)):
                        all_legal_moves.append(c)
        return len(all_legal_moves)

    # FEN used to generate position
    def fen():
        fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

        info = {'turn': 1, 'castling': [], 'en_passant': None}

        for i in fen:
            if i == ' ':
                break
            elif i.isdigit():
                fen = fen.replace(i, int(i) * '0')

        fen = fen.replace('/', '')

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

        return info

    fen_info = fen()
    turn = fen_info['turn']
    cm = fen_info['en_passant']
    bk_pos = fen_info['bk_pos']
    wk_pos = fen_info['wk_pos']

    state = board.board(fen_info['fen'])

    move_gen()

    '''
    running = True

    while running:
        if piece_selected:
            a = board.grid(event.pos[0])
            b = board.grid(event.pos[1])
            if a is not None and b is not None:
                c = str(b) + str(a)

                # Moves piece if mouse clicks at legal move
                if c in legal_moves(x, y):

                    # Removes captured pawn during en passant
                    if (state[y][x].id == 'P' and not state[b][a]
                            and x != a):
                        state[y][int(cm[2])] = None

                    # Updates position of moved piece
                    state[b][a] = state[y][x]
                    state[b][a].row, state[b][a].col = b, a
                    state[y][x] = None

                    # Promotes pawn to queen if needed
                    if state[b][a].id == 'P' and not b % 7:
                        state[b][a] = pieces.Queen(turn, b, a)

                    # Updates position of king if it was moved
                    if state[b][a].id == 'K':
                        if turn == 1:
                            wk_pos = c
                        else:
                            bk_pos = c

                        # Updates position of rook if castled
                        if abs(x - a) == 2:
                            if a == 6:
                                state[b][5] = state[b][7]
                                state[b][5].col = 5
                                state[b][7] = None
                            else:
                                state[b][3] = state[b][0]
                                state[b][3].col = 3
                                state[b][0] = None
                    turn *= -1

                    # Terminates game if stalemate or checkmate reached
                    if not all_legal_moves():
                        if turn == -1 and in_check(state, bk_pos):
                            print('white wins')
                        elif turn == 1 and in_check(state, wk_pos):
                            print('black wins')
                        else:
                            print('stalemate')
                        running = False

                    # Continues and updates game
                    else:
                        if hasattr(state[b][a], 'moved'):
                            state[b][a].moved = True
                        draw_board()
                        cm = state[b][a].id + str(y) + str(x) + c
                        print(cm)
                        piece_selected = False

                # Displays legal moves of another selected piece
                elif (state[b][a] and (a != x or b != y)
                        and state[b][a].team == turn):
                    x, y = a, b
                    move_preview(x, y)
                    piece_selected = True

                # Deselects piece
                else:
                    draw_board()
                    piece_selected = False

        # Selects piece
        else:
            x = board.grid(event.pos[0])
            y = board.grid(event.pos[1])
            if (x is not None and y is not None
                    and state[y][x] and state[y][x].team == turn):
                move_preview(x, y)
                # print(all_legal_moves())
                piece_selected = True

    # pygame.quit()
    # quit()
    '''


if __name__ == '__main__':
    main()
