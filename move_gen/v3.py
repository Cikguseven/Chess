import time

start = time.time()


def main(raw_fen, depth):

    knight_moves = [[10, 17], [11, 16, 18], [8, 12, 17, 19], [9, 13, 18, 20],
                    [10, 14, 19, 21], [11, 15, 20, 22], [12, 21, 23], [13, 22],
                    [2, 18, 25], [3, 19, 24, 26], [0, 4, 16, 20, 25, 27],
                    [1, 5, 17, 21, 26, 28], [2, 6, 18, 22, 27, 29],
                    [3, 7, 19, 23, 28, 30], [4, 20, 29, 31], [5, 21, 30],
                    [1, 10, 26, 33], [0, 2, 11, 27, 32, 34],
                    [1, 3, 8, 12, 24, 28, 33, 35],
                    [2, 4, 9, 13, 25, 29, 34, 36],
                    [3, 5, 10, 14, 26, 30, 35, 37],
                    [4, 6, 11, 15, 27, 31, 36, 38],
                    [5, 7, 12, 28, 37, 39], [6, 13, 29, 38], [9, 18, 34, 41],
                    [8, 10, 19, 35, 40, 42], [9, 11, 16, 20, 32, 36, 41, 43],
                    [10, 12, 17, 21, 33, 37, 42, 44],
                    [11, 13, 18, 22, 34, 38, 43, 45],
                    [12, 14, 19, 23, 35, 39, 44, 46], [13, 15, 20, 36, 45, 47],
                    [14, 21, 37, 46], [17, 26, 42, 49],
                    [16, 18, 27, 43, 48, 50], [17, 19, 24, 28, 40, 44, 49, 51],
                    [18, 20, 25, 29, 41, 45, 50, 52],
                    [19, 21, 26, 30, 42, 46, 51, 53],
                    [20, 22, 27, 31, 43, 47, 52, 54], [21, 23, 28, 44, 53, 55],
                    [22, 29, 45, 54], [25, 34, 50, 57],
                    [24, 26, 35, 51, 56, 58], [25, 27, 32, 36, 48, 52, 57, 59],
                    [26, 28, 33, 37, 49, 53, 58, 60],
                    [27, 29, 34, 38, 50, 54, 59, 61],
                    [28, 30, 35, 39, 51, 55, 60, 62], [29, 31, 36, 52, 61, 63],
                    [30, 37, 53, 62], [33, 42, 58], [32, 34, 43, 59],
                    [33, 35, 40, 44, 56, 60], [34, 36, 41, 45, 57, 61],
                    [35, 37, 42, 46, 58, 62], [36, 38, 43, 47, 59, 63],
                    [37, 39, 44, 60], [38, 45, 61], [41, 50], [40, 42, 51],
                    [41, 43, 48, 52], [42, 44, 49, 53], [43, 45, 50, 54],
                    [44, 46, 51, 55], [45, 47, 52], [46, 53]]

    king_moves = [[1, 8, 9], [2, 8, 9, 10, 0], [3, 9, 10, 11, 1],
                  [4, 10, 11, 12, 2], [5, 11, 12, 13, 3], [6, 12, 13, 14, 4],
                  [7, 13, 14, 15, 5], [14, 15, 6], [9, 16, 17, 0, 1],
                  [10, 16, 17, 18, 0, 1, 2, 8], [11, 17, 18, 19, 1, 2, 3, 9],
                  [12, 18, 19, 20, 2, 3, 4, 10], [13, 19, 20, 21, 3, 4, 5, 11],
                  [14, 20, 21, 22, 4, 5, 6, 12], [15, 21, 22, 23, 5, 6, 7, 13],
                  [22, 23, 6, 7, 14], [17, 24, 25, 8, 9],
                  [18, 24, 25, 26, 8, 9, 10, 16],
                  [19, 25, 26, 27, 9, 10, 11, 17],
                  [20, 26, 27, 28, 10, 11, 12, 18],
                  [21, 27, 28, 29, 11, 12, 13, 19],
                  [22, 28, 29, 30, 12, 13, 14, 20],
                  [23, 29, 30, 31, 13, 14, 15, 21], [30, 31, 14, 15, 22],
                  [25, 32, 33, 16, 17], [26, 32, 33, 34, 16, 17, 18, 24],
                  [27, 33, 34, 35, 17, 18, 19, 25],
                  [28, 34, 35, 36, 18, 19, 20, 26],
                  [29, 35, 36, 37, 19, 20, 21, 27],
                  [30, 36, 37, 38, 20, 21, 22, 28],
                  [31, 37, 38, 39, 21, 22, 23, 29], [38, 39, 22, 23, 30],
                  [33, 40, 41, 24, 25], [34, 40, 41, 42, 24, 25, 26, 32],
                  [35, 41, 42, 43, 25, 26, 27, 33],
                  [36, 42, 43, 44, 26, 27, 28, 34],
                  [37, 43, 44, 45, 27, 28, 29, 35],
                  [38, 44, 45, 46, 28, 29, 30, 36],
                  [39, 45, 46, 47, 29, 30, 31, 37], [46, 47, 30, 31, 38],
                  [41, 48, 49, 32, 33], [42, 48, 49, 50, 32, 33, 34, 40],
                  [43, 49, 50, 51, 33, 34, 35, 41],
                  [44, 50, 51, 52, 34, 35, 36, 42],
                  [45, 51, 52, 53, 35, 36, 37, 43],
                  [46, 52, 53, 54, 36, 37, 38, 44],
                  [47, 53, 54, 55, 37, 38, 39, 45], [54, 55, 38, 39, 46],
                  [49, 56, 57, 40, 41], [50, 56, 57, 58, 40, 41, 42, 48],
                  [51, 57, 58, 59, 41, 42, 43, 49],
                  [52, 58, 59, 60, 42, 43, 44, 50],
                  [53, 59, 60, 61, 43, 44, 45, 51],
                  [54, 60, 61, 62, 44, 45, 46, 52],
                  [55, 61, 62, 63, 45, 46, 47, 53], [62, 63, 46, 47, 54],
                  [57, 48, 49], [58, 48, 49, 50, 56], [59, 49, 50, 51, 57],
                  [60, 50, 51, 52, 58], [61, 51, 52, 53, 59],
                  [62, 52, 53, 54, 60], [63, 53, 54, 55, 61], [54, 55, 62]]

    # Returns algebraic coordinates of start and final position
    def an(i1, i2):
        return chr(i1 % 8 + 97) + str(8 - i1 // 8) + \
            chr(i2 % 8 + 97) + str(8 - i2 // 8)

    # Converts integer value to string with leading zero if value < 10
    def lzero(value):
        if value < 10:
            return '0' + str(value)
        return str(value)

    # Checks if king is in check
    def in_check(turn, pm, index, np, ekp, tkp, epp, tpp, flag):
        tpp = tpp.replace(lzero(index), lzero(np))

        if lzero(np) in epp:
            np_index = epp.find(lzero(np))
            epp = epp[:np_index] + epp[np_index + 3:]

        elif flag == 1:
            ep_index = epp.find(lzero(np + 8 * turn))
            epp = epp[:ep_index] + epp[ep_index + 3:]

        for i in range(len(epp) // 3):
            index = int(epp[i * 3:i * 3 + 2])
            sq = epp[i * 3 + 2]
            if (int(tkp)
                    in moves(sq, index, -turn, pm, tkp, ekp, tpp, epp, 1)[0]):
                return True

        return False

    # Generates moves of piece iteratively, including castling & en passant
    # flag = -1 for moves during own turn, flag = 1 for enemy moves
    def moves(piece, index, turn, pm, ekp, tkp, epp, tpp, flag):
        piece_id = piece.lower()
        piece_moves = []
        row = index // 8
        col = index % 8

        # Pawn moves
        if piece_id == 'p':

            # Diagonal piece capture moves
            fl = index - (9 * turn)
            fl_row = fl // 8
            if abs(fl_row - row) == 1 and (flag > 0 or lzero(fl) in epp):
                piece_moves.append(fl)

            fr = index - (7 * turn)
            fr_row = fr // 8
            if abs(fr_row - row) == 1 and (flag > 0 or lzero(fr) in epp):
                piece_moves.append(fr)

            # Forward and en passant moves during player's turn
            if flag < 0:
                fwd = index - (8 * turn)
                if lzero(fwd) not in epp + tpp:
                    piece_moves.append(fwd)

                    if (row + turn) % 7 == 0:
                        fwd2 = index - 16 * turn
                        if lzero(fwd2) not in epp + tpp:
                            piece_moves.append(fwd2)

                        return piece_moves, None

                # Generates en passant moves if available
                if pm and pm[0] == 'p':
                    ps = int(pm[1:3])
                    ns = int(pm[3:])

                    if (row == ns // 8 and abs(ps - ns) == 16
                            and abs(col - ns % 8) == 1):
                        piece_moves.append((ps + ns) // 2)

            return piece_moves, None

        # Knight moves
        elif piece_id == 'n':
            moves = knight_moves[index]

            # Inclues all squares in enemy's attack path
            if flag > 0:
                return moves, None

            return [i for i in moves if lzero(i) not in tpp], None

        # King moves
        elif piece_id == 'k':
            moves = king_moves[index]

            # Inclues all adjacent squares in enemy's attack path
            if flag > 0:
                return moves, None

            piece_moves = [i for i in moves if lzero(i) not in tpp]

            # Generates castling moves if available
            if col == 4 and not row % 7:
                left = [index - 1, index - 2, index - 3]
                right = [index + 1, index + 2]
                app = epp + tpp

                if not any(lzero(i) in app for i in left):
                    piece_moves.append(index - 2)

                if not any(lzero(i) in app for i in right):
                    piece_moves.append(index + 2)

            return piece_moves, None

        targets = []
        pinned_pieces = None

        # Only one piece can be pinned for each Bishop/Rook/Queen
        flag0 = False

        # Includes illegal square behind king in direction of Bishop/Rook/Queen
        flag1 = False

        if piece_id in {'b', 'q'}:
            targets += [-9, -7, 7, 9]

        if piece_id in {'r', 'q'}:
            targets += [-8, -1, 1, 8]

        for target in targets:

            # True if one pinned piece has been found
            flag2 = False
            temp_pinned = None
            i = index

            # Iterates through squares in direction of attack and check if\
            # square is empty or contains own/enemy pieces
            while True:
                r = i // 8
                c = i % 8

                if not ((c == 0 and target in {-9, -1, 7})
                        or (c == 7 and target in {-7, 1, 9})
                        or (r == 0 and target in {-9, -8, -7})
                        or (r == 7 and target in {7, 8, 9})):
                    i += target
                    lz_i = lzero(i)

                    if 0 <= i <= 63 and not (lz_i in tpp and flag < 0):

                        if not flag2:
                            piece_moves.append(i)

                            if flag1 or lz_i in tpp:
                                flag1 = False
                                break

                            elif lz_i in epp:

                                if flag < 0 or flag0:
                                    break

                                elif i == int(ekp):
                                    flag1 = True

                                else:
                                    temp_pinned = i
                                    flag2 = True

                        elif lzero(i) in epp:

                            if i == int(ekp):
                                pinned_pieces = temp_pinned
                                flag0 = True

                            else:
                                break

                    else:
                        break

                else:
                    break

        return piece_moves, pinned_pieces

    # Checks if move is legal (does not result in check)
    def legal_moves(piece, index, turn, pm, cstl,
                    ekp, tkp, epp, tpp, epath, pinned):
        legal_moves = []

        attacking_moves = moves(piece, index, turn, pm,
                                ekp, tkp, epp, tpp, -1)[0]

        # Removes king capturing moves
        if int(ekp) in attacking_moves:
            attacking_moves.remove(int(ekp))

        # Checks if each move is legal
        for np in attacking_moves:

            # En passant
            if (piece.lower() == 'p' and lzero(np) not in epp
                    and index % 8 != np % 8):
                if not in_check(turn, pm, index, np, ekp, tkp, epp, tpp, 1):
                    legal_moves.append(np)
                continue

            # King not in check
            if int(tkp) not in epath:

                # King is being moved
                if index == int(tkp):

                    if abs(index - np) == 2:
                        if (lzero(np) in cstl and np not in epath
                                and (index + np) // 2 not in epath):
                            legal_moves.append(np)

                    elif np not in epath:
                        legal_moves.append(np)

                # Not moving a pinned piece or legally moving a pinned piece
                elif (index not in pinned
                        or not in_check(
                        turn, pm, index, np, ekp, tkp, epp, tpp, 0)):
                    legal_moves.append(np)

            # King is in check
            else:

                # King is being moved
                if index == int(tkp):
                    if np not in epath and abs(index - np) != 2:
                        legal_moves.append(np)

                elif not in_check(turn, pm, index, np, ekp, tkp, epp, tpp, 0):
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
                j = lzero(counter)
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

        if fen[-5] in {'3', '6'}:
            col = ord(fen[-6]) - 97

            if info['turn'] == -1 and fen[-5] == '3':
                info['en_passant'] = 'p' + str(48 + col) + str(32 + col)

            elif info['turn'] == 1 and fen[-5] == '6':
                info['en_passant'] = 'p' + lzero(8 + col) + str(24 + col)

        castling_pos = {'K': '62', 'Q': '58', 'k': '06', 'q': '02'}
        i = fen.find(' ') + 3

        while True:
            if fen[i] in {' ', '-'}:
                break

            else:
                info['castling'] += castling_pos[fen[i]]
                i += 1

        return info

    # Generates number of legal moves recursively to chosen depth
    # Output is similar to Stockfish format
    def move_gen(depth, ctd, turn, pm, cstl, wkp, bkp, wpp, bpp):
        counter = 0

        # Iterates and returns all possible moves of each attacking piece

        # Assigns pieces belonging to both players
        tpp = wpp if turn > 0 else bpp
        epp = bpp if turn > 0 else wpp
        piece_count = len(tpp) // 3

        tkp = wkp if turn > 0 else bkp
        ekp = bkp if turn > 0 else wkp

        epath = set()
        pinned = set()

        # Generates squares that enemy pieces are attacking
        for i in range(len(epp) // 3):
            index = int(epp[i * 3:i * 3 + 2])
            sq = epp[i * 3 + 2]

            emoves = moves(sq, index, -turn, pm, tkp, ekp, tpp, epp, 1)
            epath |= set(emoves[0])
            if emoves[1]:
                pinned.add(emoves[1])

        # Generates possible legal moves for player moving
        for i in range(piece_count):
            index = int(tpp[i * 3:i * 3 + 2])
            sq = tpp[i * 3 + 2]
            sq_moves = legal_moves(
                sq, index, turn, pm, cstl,
                ekp, tkp, epp, tpp, epath, pinned)

            if sq_moves:
                piece_id = sq.lower()

                for np in sq_moves:

                    # Stops move generation if depth = 1
                    if depth == 1:

                        # 4 possible pieces to promote to
                        if (piece_id == 'p' and not (np // 8) % 7):
                            counter += 4
                            if depth == ctd:
                                print(f'{an(index, np)}q: 1')
                                print(f'{an(index, np)}r: 1')
                                print(f'{an(index, np)}b: 1')
                                print(f'{an(index, np)}n: 1')

                        else:
                            counter += 1
                            if depth == ctd:
                                print(f'{an(index, np)}: 1')

                    else:
                        cstl_copy = cstl
                        wkp_copy = wkp
                        bkp_copy = bkp
                        epp_copy = epp

                        # Amends board state to reflect move being made
                        lz_index = lzero(index)
                        lz_np = lzero(np)
                        tpp_copy = tpp.replace(lz_index, lz_np)

                        if lz_np in epp:
                            temp_index = epp.find(lz_np)
                            epp_copy = epp[:temp_index] + epp[temp_index + 3:]

                        elif piece_id == 'p' and index % 8 != np % 8:
                            temp_index = epp.find(lzero(np + 8 * turn))
                            epp_copy = epp[:temp_index] + epp[temp_index + 3:]

                        # Updates castling availability if rook or king moved
                        rook_pos = {63: '62', 56: '58', 7: '06', 0: '02'}
                        for i in [index, np]:
                            if rook_pos.get(i, '1') in cstl_copy:
                                cstl_copy = cstl_copy.replace(rook_pos[i], '')

                        if sq == 'K':
                            for i in ['62', '58']:
                                if i in cstl:
                                    cstl_copy = cstl_copy.replace(
                                        i, '')

                            wkp_copy = lzero(np)

                        elif sq == 'k':
                            for i in ['06', '02']:
                                if i in cstl:
                                    cstl_copy = cstl_copy.replace(
                                        i, '')

                            bkp_copy = lzero(np)

                        # Updates rook position after castling
                        if piece_id == 'k' and abs(index - np) == 2:
                            if np % 8 == 6:
                                tpp_copy = tpp_copy.replace(
                                    lzero(np + 1), lzero(np - 1))

                            else:
                                tpp_copy = tpp_copy.replace(
                                    lzero(np - 2), lzero(np + 1))

                        # Formats 'previous move' string
                        new_pm = piece_id + lz_index + lz_np

                        wpp_copy = tpp_copy if turn > 0 else epp_copy
                        bpp_copy = epp_copy if turn > 0 else tpp_copy

                        # Promotes pawn and generates moves for each
                        # possible promoted piece
                        if piece_id == 'p' and not (np // 8) % 7:
                            for i in ['Q', 'R', 'B', 'N']:

                                if turn == -1:
                                    p_index = bpp_copy.find(lzero(np)) + 2
                                    bpp_copy = bpp_copy[:p_index] + \
                                        i.lower() + bpp_copy[p_index + 1:]

                                else:
                                    p_index = wpp_copy.find(lzero(np)) + 2
                                    wpp_copy = wpp_copy[:p_index] + \
                                        i + wpp_copy[p_index + 1:]

                                # Continues with recursive move generation
                                r_depth = move_gen(depth - 1, ctd, -turn,
                                                   new_pm, cstl_copy,
                                                   wkp_copy, bkp_copy,
                                                   wpp_copy, bpp_copy)

                                if depth == ctd:
                                    print(f'{an(index, np)}{i.lower()}: '
                                          f'{r_depth}')

                                counter += r_depth
                        # Continues with recursive move generation
                        else:
                            r_depth = move_gen(depth - 1, ctd, -turn,
                                               new_pm, cstl_copy,
                                               wkp_copy, bkp_copy,
                                               wpp_copy, bpp_copy)

                            if depth == ctd:
                                print(f'{an(index, np)}: {r_depth}')

                            counter += r_depth
        return counter

    fen_info = process_fen(raw_fen)
    turn = fen_info['turn']
    pm = fen_info['en_passant']
    bkp = fen_info['bkp']
    wkp = fen_info['wkp']
    bpp = fen_info['black_piece_pos']
    wpp = fen_info['white_piece_pos']
    cstl = fen_info['castling']
    check_to_depth = depth
    print(f'go perft {depth}')

    return move_gen(depth, check_to_depth, turn, pm, cstl, wkp, bkp, wpp, bpp)


if __name__ == '__main__':

    # For testing single position
    # raw_fen = '4kN1r/Pp2n2p/8/1K1P2r1/4P3/6P1/RP2p2P/2n5 b k - 0 6'
    # depth = 1
    # print(main(raw_fen, depth))

    # For testing multiple positions
    positions = open('perft_suite.txt', 'r').read().splitlines()
    for p in positions:
        if p[0] != '#':
            depth = int(p[0])
            fen_start_index = p.rfind(',')
            raw_fen = p[fen_start_index + 1:]
            start = time.time()
            result = main(raw_fen, depth)
            end = time.time()
            duration = end - start
            print(result)
            correct_result = int(p[p.find(',') + 1:fen_start_index])
            if result == correct_result:
                print('correct')
            else:
                print('wrong')
            print(f'time taken: {duration}')
            print(f'nps: {result / 1}')
            print()
            print()

end = time.time()

print(end - start)
