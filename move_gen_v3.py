import time

start = time.time()


def main():

    # Returns algebraic coordinates of start and final position
    def an(i1, i2):
        return chr(i1 % 8 + 97) + str(8 - i1 // 8) + \
            chr(i2 % 8 + 97) + str(8 - i2 // 8)

    # # Checks if two pieces are on opposite teams
    # def is_enemy(p1, p2):
    #     if (p1.islower() and p2.isupper()) or (p1.isupper() and p2.islower()):
    #         return True
    #     return False

    # # Checks if two pieces are on the same team
    # def is_ally(p1, p2):
    #     if (p1.islower() and p2.islower()) or (p1.isupper() and p2.isupper()):
    #         return True
    #     return False

    # Changes character in string to represent piece movement
    # Necessary as strings are immutable
    def modify_str(string, index, char):
        return string[:index] + char + string[index + 1:]

        # Checks if king is in check
    def in_check(state, turn, king_pos, pm):
        for index, sq in enumerate(state):
            if (turn_check(sq, turn)
                    and king_pos in moves(sq, index, state, turn, pm, 0)):
                return True

        return False

    # Checks if piece is of the correct team
    def turn_check(piece, turn):
        if turn == 1 and piece.isupper():
            return True

        elif turn == -1 and piece.islower():
            return True
        return False

    # Generates moves of piece iteratively, including castling & en passant
    def moves(piece, index, state, turn, pm, tpp, epp, tkp, flag):
        piece_id = piece.lower()
        piece_moves = []
        row = index // 8
        col = index % 8

        if piece_id == 'p':
            fl = index - (9 * turn)
            fl_row = fl // 8
            if ((abs(fl_row - row) == 1 and 0 <= fl <= 63)
                    and (flag > 0 or str(fl) in epp)):
                piece_moves.append(fl)

            fr = index - (7 * turn)
            fr_row = fr // 8
            if ((abs(fr_row - row) == 1 and 0 <= fr <= 63)
                    and (flag > 0 or str(fr) in epp)):
                piece_moves.append(fr)

            if flag < 0:
                fwd = index - (8 * turn)
                if state[fwd] == '0' and 0 <= fwd <= 63:
                    piece_moves.append(fwd)

                    fwd2 = index - 16 * turn
                    if ((row + turn) % 7 == 0 and 0 <= fwd2 <= 63
                            and state[fwd2] == '0'):
                        piece_moves.append(fwd2)

                # Generates en passant moves (if available)
                if pm and pm[0] == 'p':
                    ps = int(pm[1:3])
                    pr = ps // 8
                    ns = int(pm[3:])
                    nr = ns // 8
                    nc = ns % 8

                    if row == nr and abs(pr - nr) == 2 and abs(col - nc) == 1:
                        piece_moves.append((ps + ns) // 2)

            return piece_moves, set()

        if piece_id == 'n':
            for target in [-17, -15, -10, -6, 6, 10, 15, 17]:
                move = index + target

                # Sum of rows and columns of old and new knight pos must be odd
                if ((row + col + move // 8 + move % 8) % 2
                        and 0 <= move <= 63
                        and str(move) not in tpp):
                    piece_moves.append(move)

            return piece_moves, set()

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
                if 0 <= move <= 63 and str(move) not in tpp:
                    piece_moves.append(move)

            # Generates castling moves (if available)
            if flag < 0 and not row % 7 and col == 4:
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

            return piece_moves, set()

        targets = []
        pinned_pieces = set()
        flag2 = False

        if piece_id in {'b', 'q'}:
            targets += [-9, -7, 7, 9]

        if piece_id in {'r', 'q'}:
            targets += [-8, -1, 1, 8]

        for target in targets:
            counter = 0
            temp_pinned = None
            i = index
            while True:
                r = i // 8
                c = i % 8
                i += target
                if (0 <= i <= 63
                    and not (str(move) in tpp
                             or (c == 0 and target in {-9, -1, 7})
                             or (c == 7 and target in {-7, 1, 9})
                             or (r == 0 and target in {-9, -8, -7})
                             or (r == 7 and target in {7, 8, 9}))):
                    if counter < 1:
                        piece_moves.append(i)
                        if str(i) in epp:
                            if flag < 1 or flag2:
                                break
                            else:
                                temp_pinned = i
                                counter += 1
                    elif counter == 1:
                        if i == ekp:
                            pinned_pieces.add(temp_pinned)
                            flag2 = True
                            break
                        elif str(i) in epp:
                            break
                else:
                    break

        return piece_moves, pinned_pieces

    # Checks if move is legal (does not result in check)
    def legal_moves(piece, index, state, turn, pm, cstl,
                    wkp, bkp, tkp, ekp, tpp, epp, e_path, pinned):
        legal_moves = []

        piece_id = piece.lower()
        attacking_moves = moves(piece, index, state, turn, pm, tpp, epp, -1)[0]

        # Removes king capturing moves
        if ekp in attacking_moves:
            attacking_moves.remove(enemy_king_pos)

        for np in attacking_moves:
            if tkp not in e_path:
                if index not in pinned:
                    legal_moves.append(np)

                else:   

            else:
                if index == tkp and np not in e_path:
                    legal_moves.append(np)

        

            king_pos = tkp

            # Tests if new position results in check
            state_copy = modify_str(state, np, piece)
            state_copy = modify_str(state_copy, index, '0')

            if (piece_id == 'p'
                    and state[np] == '0' and index % 8 != np % 8):
                state_copy = modify_str(state_copy, np + 8 * turn, '0')

            if piece_id == 'k':

                # Checks if castling is legal
                if abs(index - np) == 2:

                    if (str(np) in cstl
                            and not in_check(state, -turn, king_pos, pm)
                            and ((index + np) // 2) in legal_moves
                            and not in_check(state_copy, -turn, np, pm)):
                        legal_moves.append(np)
                    continue

                king_pos = np

            if not in_check(state_copy, -turn, king_pos, pm):
                legal_moves.append(np)

        return legal_moves

    # Obtains info from FEN to generate position
    def fen(raw_fen):
        print('position fen ' + raw_fen)

        info = {'turn': 1, 'castling': '', 'en_passant': None,
                'white_piece_pos': '', 'black_piece_pos': ''}

        raw_fen = raw_fen.replace('/', '')

        fen = ''
        counter = 0

        for i in raw_fen:
            if counter < 64:
                j = str(counter) if counter > 9 else '0' + str(counter)

                if i.isdigit():
                    counter += int(i)
                    fen += int(i) * '0'

                elif i.islower():
                    info['black_piece_pos'] += j + i
                    counter += 1
                    fen += i

                else:
                    info['white_piece_pos'] += j + i
                    counter += 1
                    fen += i
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

        castling_pos = {'K': '62', 'Q': '58', 'k': '06', 'q': '02'}
        i = 67
        while True:
            if fen[i] in {' ', '-'}:
                break

            elif fen[i] in castling_pos:
                info['castling'] += castling_pos[fen[i]]
                i += 1

        print(info)
        return info

    # Generates legal moves to chosen depth using recursion
    # Output is similar to Stockfish format
    def move_gen(depth, ctd, state, turn, pm, cstl, wkp, bkp, wpp, bpp):
        counter = 0

        # Stops move generation when depth is 0
        if depth == 0:
            return 1

        # Returns all possible moves of each attacking piece iteratively
        else:
            tpp = wpp if turn > 0 else bpp
            epp = bpp if turn > 0 else wpp
            piece_count = len(tpp) // 3

            tkp = wkp if turn > 0 else bkp
            ekp = bkp if turn > 0 else wkp

            e_path = set()
            pinned = set()

            for i in range(len(epp) // 3):
                index = int(epp[i * 3: i * 3 + 2])
                sq = epp[i * 3 + 2]
                e_moves = moves(sq, index, state, -turn,
                                pm, epp, tpp, ekp, 1)
                e_path |= set(e_moves[0])
                pinned |= set(e_moves[1])

            for i in range(piece_count):
                index = int(tpp[i * 3: i * 3 + 2])
                sq = tpp[i * 3 + 2]
                sq_moves = legal_moves(
                    sq, index, state, turn, pm, cstl,
                    wkp, bkp, tkp, ekp, tpp, epp, e_path, pinned)

                if sq_moves:
                    piece_id = sq.lower()

                    for np in sq_moves:
                        cstl_copy = cstl
                        wkp_copy = wkp
                        bkp_copy = bkp
                        wpp_copy = wpp
                        bpp_copy = bpp
                        state_copy = state

                        if (piece_id == 'p' and state[np] == '0'
                                and index % 8 != np % 8):
                            state_copy = modify_str(
                                state_copy, np + 8 * turn, '0')

                        # Amends board state to reflect move being made
                        state_copy = modify_str(state_copy, np, sq)
                        state_copy = modify_str(state_copy, index, '0')

                        # Updates cstl availability
                        rook_pos = {63: '62', 56: '58', 7: '06', 0: '02'}
                        rook_sq = [np, index]
                        for pos in rook_sq:
                            if (pos in rook_pos and rook_pos[pos] in
                                    cstl_copy):
                                cstl_copy = cstl_copy.replace(
                                    rook_pos[pos], '')

                        if sq == 'K':
                            for wkc in ['62', '58']:
                                if wkc in cstl_copy:
                                    cstl_copy = cstl_copy.replace(
                                        wkc, '')

                            wkp_copy = np

                        elif sq == 'k':
                            for bkc in ['06', '02']:
                                if bkc in cstl_copy:
                                    cstl_copy = cstl_copy.replace(
                                        bkc, '')

                            bkp_copy = np

                        # Updates rook position after cstl
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
                        pm_str = [index, np]

                        for i, value in enumerate(pm_str):
                            if value < 10:
                                pm_str[i] = '0' + str(value)
                            else:
                                pm_str[i] = str(value)

                        new_pm = piece_id + pm_str[0] + pm_str[1]

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
                                                   new_pm, cstl_copy,
                                                   wkp_copy, bkp_copy,
                                                   wpp_copy, bpp_copy)

                                if depth == ctd:
                                    print(f'{an(index, np)}{p}: {r_depth}')

                                counter += r_depth
                        # Continues with recursive move generation
                        else:
                            r_depth = move_gen(depth - 1, ctd,
                                               state_copy, -turn,
                                               new_pm, cstl_copy,
                                               wkp_copy, bkp_copy,
                                               wpp_copy, bpp_copy)

                            if depth == ctd:
                                print(f'{an(index, np)}: {r_depth}')

                            counter += r_depth
        return counter

    # Input FEN of position
    test = 'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1'

    fen_info = fen(test)
    turn = fen_info['turn']
    pm = fen_info['en_passant']
    bkp = fen_info['bkp']
    wkp = fen_info['wkp']
    bpp = fen_info['black_piece_pos']
    wpp = fen_info['white_piece_pos']
    cstl = fen_info['castling']
    state = fen_info['fen'][:64]
    depth = 3
    check_to_depth = depth

    w_att =

    print(move_gen(depth, check_to_depth, state,
                   turn, pm, cstl, wkp, bkp, wpp, bpp))


if __name__ == '__main__':
    main()

end = time.time()

print(end - start)
