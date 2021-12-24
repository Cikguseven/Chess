from copy import deepcopy


def main():

    # Returns algebraic coordinates of start and final position
    def an(i1, i2):
        return chr(i1 % 8 + 97) + str(8 - i1 // 8) + \
            chr(i2 % 8 + 97) + str(8 - i2 // 8)

    # Checks if two pieces are on opposite teams
    def is_enemy(p1, p2):
        if (p1.islower() and p2.isupper()) or (p1.isupper() and p2.islower()):
            return True
        return False

    # Checks if two pieces are on the same team
    def is_ally(p1, p2):
        if (p1.islower() and p2.islower()) or (p1.isupper() and p2.isupper()):
            return True
        return False

    # Changes character in string to represent piece movement
    # Necessary as strings are immutable
    def modify_str(string, index, char):
        return string[:index] + char + string[index + 1:]

    # Generates moves of piece iteratively, including castling & en passant
    def moves(piece, index, state, turn, pm, flag):
        piece_id = piece.lower()
        piece_moves = []
        row = index // 8
        col = index % 8

        if piece_id == 'p':
            fl = index - (9 * turn)
            fl_row = fl // 8
            if (abs(fl_row - row) == 1 and 0 <= fl <= 63
                    and is_enemy(piece, state[fl])):
                piece_moves.append(fl)

            fr = index - (7 * turn)
            fr_row = fr // 8
            if (abs(fr_row - row) == 1 and 0 <= fr <= 63
                    and is_enemy(piece, state[fr])):
                piece_moves.append(fr)

            fwd = index - (8 * turn)
            if 0 <= fwd <= 63 and state[fwd] == '0':
                piece_moves.append(fwd)

                if ((row + turn) % 7 == 0 and 0 <= index - 16 * turn <= 63
                        and state[index - 16 * turn] == '0'):
                    piece_moves.append(index - 16 * turn)

            # Generates en passant moves (if available)
            if flag and pm and pm[0] == 'p':
                ps = int(pm[1:3])
                pr = ps // 8
                ns = int(pm[3:])
                nr = ns // 8
                nc = ns % 8

                if row == nr and abs(pr - nr) == 2 and abs(col - nc) == 1:
                    piece_moves.append((ps + ns) // 2)

            return piece_moves

        if piece_id == 'n':
            for target in [-17, -15, -10, -6, 6, 10, 15, 17]:
                move = index + target

                # Sum of rows and columns of old and new knight pos must be odd
                if ((row + col + move // 8 + move % 8) % 2
                        and 0 <= move <= 63
                        and not is_ally(piece, state[move])):
                    piece_moves.append(move)

            return piece_moves

        if piece_id == 'k':
            targets = {-9, -8, -7, -1, 1, 7, 8, 9}

            if col == 0:
                targets -= {-9, -1, 7}
            elif col == 7:
                targets -= {-7, 1, 9}
            if row == 0:
                targets -= {-9, -8, -7}
            elif row == 7:
                targets -= {7, 8, 9}

            for target in targets:
                move = index + target
                if 0 <= move <= 63 and not is_ally(piece, state[move]):
                    piece_moves.append(move)

            # Generates castling moves (if available)
            if flag and not row % 7 and col == 4:
                l1 = state[index - 1]
                l2 = state[index - 2]
                l3 = state[index - 3]
                l4 = state[index - 4]
                r1 = state[index + 1]
                r2 = state[index + 2]
                r3 = state[index + 3]

                if l1 == l2 == l3 == '0' and l4 in {'r', 'R'}:
                    piece_moves.append(index - 2)

                if r1 == r2 == '0' and r3 in {'r', 'R'}:
                    piece_moves.append(index + 2)
            return piece_moves

        targets = []

        if piece_id in {'b', 'q'}:
            targets += [-9, -7, 7, 9]

        if piece_id in {'r', 'q'}:
            targets += [-8, -1, 1, 8]

        for target in targets:
            i = index
            while True:
                i_row = i // 8
                i_col = i % 8
                i += target

                if (0 <= i <= 63 and not is_ally(piece, state[i])
                        and not (i_col == 0 and target in {-9, -1, 7})
                        and not (i_col == 7 and target in {-7, 1, 9})
                        and not (i_row == 0 and target in {-9, -8, -7})
                        and not (i_row == 7 and target in {7, 8, 9})):
                    piece_moves.append(i)
                    if is_enemy(piece, state[i]):
                        break
                else:
                    break

        return piece_moves

    # Checks if move is legal (does not result in check)
    def legal_moves(piece, index, state, turn, pm, castling, wkp, bkp):
        legal_moves = []

        piece_id = piece.lower()

        for np in moves(piece, index, state, turn, pm, True):
            state_copy = state
            king_pos = wkp if turn > 0 else bkp
            enemy_king_pos = bkp if turn > 0 else wkp

            # Removes king capturing moves
            if np != enemy_king_pos:

                if (piece_id == 'p'
                        and state[np] == '0' and index % 8 != np % 8):
                    state_copy = modify_str(state_copy, np + 8 * turn, '0')

                # Tests if new position results in check
                state_copy = modify_str(state_copy, np, piece)
                state_copy = modify_str(state_copy, index, '0')

                if piece_id == 'k':

                    # Checks if castling is legal
                    if abs(index - np) == 2:

                        if (np in castling
                                and not in_check(state, -turn, king_pos, pm)
                                and ((index + np) // 2) in legal_moves
                                and not in_check(state_copy, -turn, np, pm)):
                            legal_moves.append(np)
                        continue

                    king_pos = np

                if not in_check(state_copy, -turn, king_pos, pm):
                    legal_moves.append(np)

        return legal_moves

    # Checks if king is in check
    def in_check(state, turn, king_pos, pm):
        for index, sq in enumerate(state):
            if (turn_check(sq, turn)
                    and king_pos in moves(sq, index, state, turn, pm, False)):
                return True

        return False

    # Checks if piece is of the correct team
    def turn_check(piece, turn):
        if turn == 1 and piece.isupper():
            return True

        elif turn == -1 and piece.islower():
            return True
        return False

    # Obtains info from FEN to generate position
    def fen(raw_fen):
        # print('position fen ' + raw_fen)

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

        info['bkp'] = fen.index('k')
        info['wkp'] = fen.index('K')

        if fen[-5] == '3' or fen[-5] == '6':
            col = ord(fen[-6]) - 97
            if fen[65] == 'b' and fen[-5] == '3':
                info['en_passant'] = 'p' + str(48 + col) + str(32 + col)

            elif fen[65] == 'w' and fen[-5] == '6':
                info['en_passant'] = 'p' + str(8 + col) + str(24 + col)

        castling_pos = {'K': 62, 'Q': 58, 'k': 6, 'q': 2}
        i = 67
        while True:
            j = fen[i]
            if j == ' ' or j == '-':
                break

            elif j in castling_pos:
                info['castling'].append(castling_pos[j])
                i += 1
        return info

    # Generates legal moves to chosen depth using recursion
    # Output is similar to Stockfish format
    def move_gen(depth, ctd, state, turn, pm, castling, wkp, bkp):
        counter = 0

        # Stops move generation when depth is 0
        if depth == 0:
            return 1

        # Returns all possible moves of each attacking piece iteratively
        else:
            for index, sq in enumerate(state):
                if turn_check(sq, turn):
                    sq_moves = legal_moves(
                        sq, index, state, turn, pm, castling, wkp, bkp)
                    if sq_moves:
                        piece_id = sq.lower()

                        for np in sq_moves:
                            castling_copy = deepcopy(castling)
                            wkp_copy = wkp
                            bkp_copy = bkp
                            state_copy = state

                            if (piece_id == 'p' and state[np] == '0'
                                    and index % 8 != np % 8):
                                state_copy = modify_str(
                                    state_copy, np + 8 * turn, '0')

                            # Amends board state to reflect move being made
                            state_copy = modify_str(state_copy, np, sq)
                            state_copy = modify_str(state_copy, index, '0')

                            # Updates castling availability
                            rook_pos = {0: 2, 7: 6, 56: 58, 63: 62}
                            rook_sq = [np, index]
                            for pos in rook_sq:
                                if (pos in rook_pos and rook_pos[pos] in
                                        castling_copy):
                                    castling_copy.remove(rook_pos[pos])

                            if sq == 'K':
                                for wkc in [58, 62]:
                                    if wkp_copy == 60 and wkc in castling_copy:
                                        castling_copy.remove(wkc)

                                wkp_copy = np

                            elif sq == 'k':
                                for bkc in [2, 6]:
                                    if bkp_copy == 4 and bkc in castling_copy:
                                        castling_copy.remove(bkc)

                                bkp_copy = np

                            # Updates rook position after castling
                            if piece_id == 'k' and abs(index - np) == 2:
                                if np % 8 == 6:
                                    state_copy = modify_str(
                                        state_copy, np - 1, state_copy[np + 1])

                                    state_copy = modify_str(
                                        state_copy, np + 1, '0')

                                else:
                                    state_copy = modify_str(
                                        state_copy, np + 1, state_copy[np - 2])

                                    state_copy = modify_str(
                                        state_copy, np - 2, '0')

                            # Formats 'previous move' string
                            to_str = [index, np]

                            for i, value in enumerate(to_str):
                                if value < 10:
                                    to_str[i] = '0' + str(value)
                                else:
                                    to_str[i] = str(value)

                            new_pm = piece_id + to_str[0] + to_str[1]

                            # Promotes pawn and generates moves for each
                            # possible promoted piece
                            if piece_id == 'p' and not (np // 8) % 7:
                                promotion = ['Q', 'B', 'R', 'N']
                                for p in promotion:
                                    if turn == -1:
                                        p = p.lower()

                                    state_p = modify_str(state_copy, np, p)

                                    # Continues with recursive move generation
                                    r_depth = move_gen(depth - 1, ctd,
                                                       state_p, -turn,
                                                       new_pm, castling_copy,
                                                       wkp_copy, bkp_copy)

                                    if depth == ctd:
                                        print(f'{an(index, np)}{p}: {r_depth}')

                                    counter += r_depth
                            # Continues with recursive move generation
                            else:
                                r_depth = move_gen(depth - 1, ctd,
                                                   state_copy, -turn,
                                                   new_pm, castling_copy,
                                                   wkp_copy, bkp_copy)

                                if depth == ctd:
                                    print(f'{an(index, np)}: {r_depth}')

                                counter += r_depth
            return counter

    # Input FEN of position
    test = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

    fen_info = fen(test)
    turn = fen_info['turn']
    pm = fen_info['en_passant']
    bkp = fen_info['bkp']
    wkp = fen_info['wkp']
    castling = fen_info['castling']
    state = fen_info['fen'][:64]
    check_to_depth = 3

    print(move_gen(3, check_to_depth, state, turn, pm, castling, wkp, bkp))


if __name__ == '__main__':
    main()
