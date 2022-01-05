import time

start = time.time()


def main():

    # Returns algebraic coordinates of start and final position
    def an(i1, i2):
        return chr(i1 % 8 + 97) + str(8 - i1 // 8) + \
            chr(i2 % 8 + 97) + str(8 - i2 // 8)

    def l_zero(value):
        if value < 10:
            return '0' + str(value)
        return str(value)

    # Changes character in string to represent piece movement
    # Necessary as strings are immutable
    def modify_str(string, index, char):
        return string[:index] + char + string[index + 1:]

    # Checks if king is in check
    def in_check(turn, pm, index, np, ekp, tkp, epp, tpp):
        tpp = tpp.replace(l_zero(index), l_zero(np))

        if l_zero(np) in epp:
            np_index = epp.find(l_zero(np))
            epp = epp[:np_index] + epp[np_index + 3:]

        for i in range(len(epp) // 3):
            index = int(epp[i * 3:i * 3 + 2])
            sq = epp[i * 3 + 2]
            a = moves(sq, index, -turn, pm, tkp, ekp, tpp, epp, 1)[0]

            if int(tkp) in a:
                return True

        return False

    # Generates moves of piece iteratively, including castling & en passant
    # flag = -1 for moves during own turn. flag = 1 for enemy moves
    def moves(piece, index, turn, pm, ekp, tkp, epp, tpp, flag):
        piece_id = piece.lower()
        piece_moves = []
        row = index // 8
        col = index % 8

        if piece_id == 'p':
            fl = index - (9 * turn)
            fl_row = fl // 8
            if (abs(fl_row - row) == 1 and 0 <= fl <= 63
                    and (flag > 0 or l_zero(fl) in epp)):
                piece_moves.append(fl)

            fr = index - (7 * turn)
            fr_row = fr // 8
            if (abs(fr_row - row) == 1 and 0 <= fr <= 63
                    and (flag > 0 or l_zero(fr) in epp)):
                piece_moves.append(fr)

            if flag < 0:
                fwd = index - (8 * turn)
                if (l_zero(fwd) not in epp
                        and l_zero(fwd) not in tpp
                        and 0 <= fwd <= 63):
                    piece_moves.append(fwd)

                    fwd2 = index - 16 * turn
                    if ((row + turn) % 7 == 0 and 0 <= fwd2 <= 63
                            and l_zero(fwd2) not in epp
                            and l_zero(fwd2) not in tpp):
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

        elif piece_id == 'n':
            for target in [-17, -15, -10, -6, 6, 10, 15, 17]:
                move = index + target

                # Sum of rows and columns of old and new knight pos must be odd
                if ((row + col + move // 8 + move % 8) % 2
                        and 0 <= move <= 63
                        and l_zero(move) not in tpp):
                    piece_moves.append(move)

            return piece_moves, set()

        elif piece_id == 'k':
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
                if l_zero(move) not in tpp:
                    piece_moves.append(move)

            # Generates castling moves (if available)
            if flag < 0 and not row % 7 and col == 4:
                left = [index - 1, index - 2, index - 3]
                right = [index + 1, index + 2]

                if not any(l_zero(i) in tpp + epp for i in left):
                    piece_moves.append(index - 2)

                if not any(l_zero(i) in tpp + epp for i in right):
                    piece_moves.append(index + 2)

            return piece_moves, set()

        targets = []
        pinned_pieces = set()

        # Only needs to find one pinned piece
        flag0 = False

        # Continues checking for illegal squares in direction of piece's path
        flag1 = False

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
                    and not (l_zero(i) in tpp
                             or (c == 0 and target in {-9, -1, 7})
                             or (c == 7 and target in {-7, 1, 9})
                             or (r == 0 and target in {-9, -8, -7})
                             or (r == 7 and target in {7, 8, 9}))):
                    if counter < 1 or flag1:
                        piece_moves.append(i)
                        if flag1:
                            flag1 = False
                            break
                        elif l_zero(i) in epp:
                            if flag < 1 or flag0:
                                break
                            elif i == int(ekp):
                                flag1 = True
                            else:
                                temp_pinned = i
                                counter += 1
                    elif counter == 1:
                        if i == int(ekp):
                            pinned_pieces.add(temp_pinned)
                            flag0 = True
                            break
                        elif l_zero(i) in epp:
                            break
                else:
                    break
        return piece_moves, pinned_pieces

    # Checks if move is legal (does not result in check)
    def legal_moves(piece, index, turn, pm, cstl,
                    wkp, bkp, ekp, tkp, epp, tpp, epath, pinned):
        legal_moves = []

        attacking_moves = moves(piece, index, turn, pm,
                                ekp, tkp, epp, tpp, -1)[0]

        # Removes king capturing moves
        if int(ekp) in attacking_moves:
            attacking_moves.remove(int(ekp))

        # Checks if each move is legal
        for np in attacking_moves:

            # En passant
            if (piece.lower() == 'p' and l_zero(np) not in epp
                    and l_zero(np) not in tpp and index % 8 != np % 8
                    and index not in pinned):
                legal_moves.append(np)
                continue

            # King not in check
            if int(tkp) not in epath:

                # King is being moved
                if index == int(tkp):

                    if abs(index - np) == 2:
                        if (l_zero(np) in cstl and np not in epath
                                and (index + np) // 2 not in epath):
                            legal_moves.append(np)

                    elif np not in epath:
                        legal_moves.append(np)

                # Not moving a pinned piece
                elif index not in pinned:
                    legal_moves.append(np)

                # Check if moving a pinned piece is legal
                elif not in_check(turn, pm, index, np, ekp, tkp, epp, tpp):
                    legal_moves.append(np)

            # King is in check
            else:

                # King is being moved
                if index == int(tkp):
                    if np not in epath and abs(index - np) != 2:
                        legal_moves.append(np)

                elif not in_check(turn, pm, index, np, ekp, tkp, epp, tpp):
                    legal_moves.append(np)

        return legal_moves

    # Obtains info from FEN to generate position
    def process_fen(fen):
        print('position fen ' + fen)

        info = {'turn': 1, 'castling': '', 'en_passant': None,
                'white_piece_pos': '', 'black_piece_pos': ''}

        fen = fen.replace('/', '')

        counter = 0

        for i in fen:
            if counter < 64:
                j = l_zero(counter)
                if i.isdigit():
                    counter += int(i)

                elif i.islower():
                    info['black_piece_pos'] += j + i
                    if i == 'k':
                        info['bkp'] = j
                    counter += 1

                else:
                    info['white_piece_pos'] += j + i
                    if i == 'K':
                        info['wkp'] = j
                    counter += 1

            else:
                break

        if fen[fen.find(' ') + 1] == 'b':
            info['turn'] = -1

        if fen[-5] == '3' or fen[-5] == '6':
            col = ord(fen[-6]) - 97

            if info['turn'] == -1 and fen[-5] == '3':
                info['en_passant'] = 'p' + str(48 + col) + str(32 + col)

            elif info['turn'] == 1 and fen[-5] == '6':
                info['en_passant'] = 'p' + l_zero(8 + col) + str(24 + col)

        castling_pos = {'K': '62', 'Q': '58', 'k': '06', 'q': '02'}
        i = fen.find(' ') + 3

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
    def move_gen(depth, ctd, turn, pm, cstl, wkp, bkp, wpp, bpp):
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

            epath = set()
            pinned = set()

            for i in range(len(epp) // 3):
                index = int(epp[i * 3:i * 3 + 2])
                sq = epp[i * 3 + 2]

                emoves = moves(sq, index, -turn, pm, tkp, ekp, tpp, epp, 1)
                epath |= set(emoves[0])
                pinned |= set(emoves[1])

            for i in range(piece_count):
                index = int(tpp[i * 3:i * 3 + 2])
                sq = tpp[i * 3 + 2]
                sq_moves = legal_moves(
                    sq, index, turn, pm, cstl,
                    wkp, bkp, ekp, tkp, epp, tpp, epath, pinned)

                if sq_moves:
                    piece_id = sq.lower()

                    for np in sq_moves:
                        cstl_copy = cstl
                        wkp_copy = wkp
                        bkp_copy = bkp
                        epp_copy = epp

                        # Amends board state to reflect move being made
                        lz_index = l_zero(index)
                        lz_np = l_zero(np)
                        tpp_copy = tpp.replace(lz_index, lz_np)

                        if lz_np in epp:
                            temp_index = epp.find(lz_np)
                            epp_copy = epp[:temp_index] + epp[temp_index + 3:]

                        elif (piece_id == 'p' and index % 8 != np % 8
                                and lz_np not in tpp and lz_np not in epp):
                            temp_index = epp.find(l_zero(np + 8 * turn))
                            epp_copy = epp[:temp_index] + epp[temp_index + 3:]

                        # Updates castling availability
                        rook_pos = {63: '62', 56: '58', 7: '06', 0: '02'}
                        rook_sq = [np, index]
                        for i in rook_sq:
                            if (i in rook_pos and rook_pos[i] in
                                    cstl_copy):
                                cstl_copy = cstl_copy.replace(
                                    rook_pos[i], '')

                        if sq == 'K':
                            for i in ['62', '58']:
                                if i in cstl_copy:
                                    cstl_copy = cstl_copy.replace(
                                        i, '')

                            wkp_copy = l_zero(np)

                        elif sq == 'k':
                            for i in ['06', '02']:
                                if i in cstl_copy:
                                    cstl_copy = cstl_copy.replace(
                                        i, '')

                            bkp_copy = l_zero(np)

                        # Updates rook position after castling
                        if piece_id == 'k' and abs(index - np) == 2:
                            if np % 8 == 6:
                                tpp_copy = tpp_copy.replace(
                                    l_zero(np + 1), l_zero(np - 1))

                            else:
                                tpp_copy = tpp_copy.replace(
                                    l_zero(np - 2), l_zero(np + 1))

                        # Formats 'previous move' string
                        new_pm = piece_id + lz_index + lz_np

                        # Promotes pawn and generates moves for each
                        # possible promoted piece
                        if piece_id == 'p' and not (np // 8) % 7:
                            promotion = ['Q', 'B', 'R', 'N']
                            for i in promotion:
                                if turn == -1:
                                    i = i.lower()

                                tpp_copy = modify_str(
                                    tpp_copy, tpp_copy.find(l_zero(np)) + 2, i)

                                wpp_copy = tpp_copy if turn > 0 else epp_copy
                                bpp_copy = epp_copy if turn > 0 else tpp_copy

                                # Continues with recursive move generation
                                r_depth = move_gen(depth - 1, ctd, -turn,
                                                   new_pm, cstl_copy,
                                                   wkp_copy, bkp_copy,
                                                   wpp_copy, bpp_copy)

                                if depth == ctd:
                                    print(f'{an(index, np)}{i}: {r_depth}')

                                counter += r_depth
                        # Continues with recursive move generation
                        else:
                            wpp_copy = tpp_copy if turn > 0 else epp_copy
                            bpp_copy = epp_copy if turn > 0 else tpp_copy

                            r_depth = move_gen(depth - 1, ctd, -turn,
                                               new_pm, cstl_copy,
                                               wkp_copy, bkp_copy,
                                               wpp_copy, bpp_copy)

                            if depth == ctd:
                                print(f'{an(index, np)}: {r_depth}')

                            counter += r_depth
        return counter

    # Input FEN of position
    test = 'r3k2r/p1ppqNb1/bn2p1p1/3n4/1p2P3/2N2Q1p/PPPBBPPP/1R2K2R b Kkq - 0 1'

    fen_info = process_fen(test)
    turn = fen_info['turn']
    pm = fen_info['en_passant']
    bkp = fen_info['bkp']
    wkp = fen_info['wkp']
    bpp = fen_info['black_piece_pos']
    wpp = fen_info['white_piece_pos']
    cstl = fen_info['castling']
    depth = 1
    check_to_depth = depth
    print(f'depth: {depth}')

    print(move_gen(depth, check_to_depth, turn, pm, cstl, wkp, bkp, wpp, bpp))


if __name__ == '__main__':
    main()

end = time.time()

print(end - start)

# Add defended pieces
