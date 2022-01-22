from v4_pieces import *
from v4_board import *


import time

start = time.time()


def main():
    # Returns algebraic coordinates of start and final position
    def an(pos):
        return chr(pos % 8 + 97) + str(8 - pos // 8)

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
            for target in [-17, -15, -10, -6, 6, 10, 15, 17]:
                move = index + target

                if move > 63:
                    break

                # Sum of rows and columns of old and new knight pos must be odd
                elif (move >= 0 and (row + col + move // 8 + move % 8) % 2
                        and (flag > 0 or lzero(move) not in tpp)):
                    piece_moves.append(move)

            return piece_moves, None

        # King moves
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

            # Inclues all adjacent squares in enemy's attack path
            if flag > 0:
                piece_moves = [index + i for i in targets]

            else:
                piece_moves = [
                    index + i for i in targets if lzero(index + i) not in tpp]

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

            # Iterates through squares in direction of attack and check if
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

            if info['turn'] == -1:
                info['en_passant'] = 'p' + str(48 + col) + str(32 + col)

            elif info['turn'] == 1:
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
                        counter += 1

                        # 4 possible pieces to promote to
                        if (piece_id == 'p' and not (np // 8) % 7):
                            counter += 3

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
                                    print(f'{an(index, np)}{i}: {r_depth}')

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

    # Input FEN of position
    test = 'r3k2r/pp3pp1/PN1pr1p1/4p1P1/4P3/3P4/P1P2PP1/R3K2R w KQkq - 4 4'

    fen_info = process_fen(test)
    turn = fen_info['turn']
    pm = fen_info['en_passant']
    bkp = fen_info['bkp']
    wkp = fen_info['wkp']
    bpp = fen_info['black_piece_pos']
    wpp = fen_info['white_piece_pos']
    cstl = fen_info['castling']
    depth = 4
    check_to_depth = depth
    print(f'go perft {depth}')

    print(move_gen(depth, check_to_depth, turn, pm, cstl, wkp, bkp, wpp, bpp))


if __name__ == '__main__':
    main()

    # For testing multiple positions
    # positions = open('perft_benchmark.txt', 'r').read().splitlines()
    # for p in positions:
    #     if p[0] != '#':
    #         depth = int(p[0])
    #         fen_start_index = p.rfind(',')
    #         raw_fen = p[fen_start_index + 1:]
    #         start = time.time()
    #         result = main(raw_fen, depth)
    #         end = time.time()
    #         duration = end - start
    #         print(result)
    #         print(duration)
    #         print(result / duration)
    #         print()
    #         print()

end = time.time()

print(end - start)
