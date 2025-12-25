from engine.sliders import bishop_attacks, queen_attacks, rook_attacks
from .position import Position, PIECE_TO_INDEX
from .attacks import KNIGHT_ATTACKS, KING_ATTACKS, FILE_A, FILE_H, RANK_2, RANK_7, RANK_1, RANK_8
from .bitboard import pop_lsb
from .move import Move

MASK64 = 0xFFFFFFFFFFFFFFFF
PROMOS = ("q", "r", "b", "n")

def generate_knight_moves(pos: Position) -> list[Move]:
    moves: list[Move] = []

    if pos.side_to_move == "w":
        knights = pos.pieces[PIECE_TO_INDEX["N"]]
        own_occ = pos.white_occ
        enemy_occ = pos.black_occ
    else:
        knights = pos.pieces[PIECE_TO_INDEX["n"]]
        own_occ = pos.black_occ
        enemy_occ = pos.white_occ

    bb = knights
    while bb:
        from_sq, bb = pop_lsb(bb)
        
        attacks = KNIGHT_ATTACKS[from_sq]
        
        targets = attacks & ~own_occ

        t = targets
        while t:
            to_sq, t = pop_lsb(t)
            moves.append(Move(from_sq, to_sq))

    return moves

def generate_king_moves(pos: Position) -> list[Move]:
    moves: list[Move] = []

    if pos.side_to_move == "w":
        king_bb = pos.pieces[PIECE_TO_INDEX["K"]]
        own_occ = pos.white_occ
    else:
        king_bb = pos.pieces[PIECE_TO_INDEX["k"]]
        own_occ = pos.black_occ
    
    if king_bb == 0:
        return moves
    
    from_sq, _ = pop_lsb(king_bb)
    targets = KING_ATTACKS[from_sq] & ~own_occ

    t = targets
    while t:
        to_sq, t = pop_lsb(t)
        moves.append(Move(from_sq, to_sq))

    return moves

def generate_pawn_moves(pos: Position) -> list[Move]:
    moves: list[Move] = []
    empty = (~pos.all_occ) & MASK64

    if pos.side_to_move == "w":
        pawns = pos.pieces[PIECE_TO_INDEX["P"]]
        enemy = pos.black_occ

        # --- Single pushes ---
        single_targets = (pawns << 8) & empty

        promo_pushes = single_targets & RANK_8
        quiet_pushes = single_targets & ~RANK_8

        t = quiet_pushes
        while t:
            to_sq, t = pop_lsb(t)
            moves.append(Move(to_sq - 8, to_sq))

        t = promo_pushes
        while t:
            to_sq, t = pop_lsb(t)
            from_sq = to_sq - 8
            for p in PROMOS:
                moves.append(Move(from_sq, to_sq, p))

        # --- Double pushes (never promotions) ---
        rank3_targets = ((pawns & RANK_2) << 8) & empty
        double_targets = (rank3_targets << 8) & empty

        dt = double_targets
        while dt:
            to_sq, dt = pop_lsb(dt)
            moves.append(Move(to_sq - 16, to_sq))

        # --- Captures ---
        captures_left  = ((pawns & ~FILE_A) << 7) & enemy   # NW
        captures_right = ((pawns & ~FILE_H) << 9) & enemy   # NE

        promo_caps_l = captures_left & RANK_8
        promo_caps_r = captures_right & RANK_8
        caps_l = captures_left & ~RANK_8
        caps_r = captures_right & ~RANK_8

        cl = caps_l
        while cl:
            to_sq, cl = pop_lsb(cl)
            moves.append(Move(to_sq - 7, to_sq))

        cr = caps_r
        while cr:
            to_sq, cr = pop_lsb(cr)
            moves.append(Move(to_sq - 9, to_sq))

        cl = promo_caps_l
        while cl:
            to_sq, cl = pop_lsb(cl)
            from_sq = to_sq - 7
            for p in PROMOS:
                moves.append(Move(from_sq, to_sq, p))

        cr = promo_caps_r
        while cr:
            to_sq, cr = pop_lsb(cr)
            from_sq = to_sq - 9
            for p in PROMOS:
                moves.append(Move(from_sq, to_sq, p))

        # --- En passant ---
        if pos.ep_square is not None:
            ep_bb = 1 << pos.ep_square

            # White captures to ep square from:
            # - down-left (from_sq = ep - 7) means pawn came from one file right (e.g. e5 -> d6)
            # - down-right (from_sq = ep - 9)
            #
            # Another way: generate the pawn capture target squares and see if ep square is among them.
            ep_from_left  = ((pawns & ~FILE_A) << 7) & ep_bb   # pawn that could capture NW onto ep
            ep_from_right = ((pawns & ~FILE_H) << 9) & ep_bb   # pawn that could capture NE onto ep

            if ep_from_left:
                # if ep_from_left is nonzero, there is exactly one pawn that can do it
                from_sq = pos.ep_square - 7
                moves.append(Move(from_sq, pos.ep_square))

            if ep_from_right:
                from_sq = pos.ep_square - 9
                moves.append(Move(from_sq, pos.ep_square))


    else:
        pawns = pos.pieces[PIECE_TO_INDEX["p"]]
        enemy = pos.white_occ

        # --- Single pushes ---
        single_targets = (pawns >> 8) & empty

        promo_pushes = single_targets & RANK_1
        quiet_pushes = single_targets & ~RANK_1

        t = quiet_pushes
        while t:
            to_sq, t = pop_lsb(t)
            moves.append(Move(to_sq + 8, to_sq))

        t = promo_pushes
        while t:
            to_sq, t = pop_lsb(t)
            from_sq = to_sq + 8
            for p in PROMOS:
                moves.append(Move(from_sq, to_sq, p))

        # --- Double pushes ---
        rank6_targets = ((pawns & RANK_7) >> 8) & empty
        double_targets = (rank6_targets >> 8) & empty

        dt = double_targets
        while dt:
            to_sq, dt = pop_lsb(dt)
            moves.append(Move(to_sq + 16, to_sq))

        # --- Captures ---
        captures_left  = ((pawns & ~FILE_A) >> 9) & enemy   # SW
        captures_right = ((pawns & ~FILE_H) >> 7) & enemy   # SE

        promo_caps_l = captures_left & RANK_1
        promo_caps_r = captures_right & RANK_1
        caps_l = captures_left & ~RANK_1
        caps_r = captures_right & ~RANK_1

        cl = caps_l
        while cl:
            to_sq, cl = pop_lsb(cl)
            moves.append(Move(to_sq + 9, to_sq))

        cr = caps_r
        while cr:
            to_sq, cr = pop_lsb(cr)
            moves.append(Move(to_sq + 7, to_sq))

        cl = promo_caps_l
        while cl:
            to_sq, cl = pop_lsb(cl)
            from_sq = to_sq + 9
            for p in PROMOS:
                moves.append(Move(from_sq, to_sq, p))

        cr = promo_caps_r
        while cr:
            to_sq, cr = pop_lsb(cr)
            from_sq = to_sq + 7
            for p in PROMOS:
                moves.append(Move(from_sq, to_sq, p))

        # --- En passant ---
        if pos.ep_square is not None:
            ep_bb = 1 << pos.ep_square

            # Black captures "down" (towards decreasing ranks), but our shifts already encode that.
            # Black pawn capture targets are:
            # - >> 9 (from pawn perspective) and >> 7
            ep_from_left  = ((pawns & ~FILE_A) >> 9) & ep_bb
            ep_from_right = ((pawns & ~FILE_H) >> 7) & ep_bb

            if ep_from_left:
                from_sq = pos.ep_square + 9
                moves.append(Move(from_sq, pos.ep_square))

            if ep_from_right:
                from_sq = pos.ep_square + 7
                moves.append(Move(from_sq, pos.ep_square))


    return moves


def generate_rook_moves(pos: Position) -> list[Move]:
    moves: list[Move] = []

    if pos.side_to_move == "w":
        rooks = pos.pieces[PIECE_TO_INDEX["R"]]
        own_occ = pos.white_occ
    else:
        rooks = pos.pieces[PIECE_TO_INDEX["r"]]
        own_occ = pos.black_occ

    bb = rooks
    while bb:
        from_sq, bb = pop_lsb(bb)
        attacks = rook_attacks(from_sq, pos.all_occ)
        targets = attacks & ~own_occ

        t = targets
        while t:
            to_sq, t = pop_lsb(t)
            moves.append(Move(from_sq, to_sq))

    return moves

def generate_bishop_moves(pos: Position) -> list[Move]:
    moves: list[Move] = []

    if pos.side_to_move == "w":
        bishops = pos.pieces[PIECE_TO_INDEX["B"]]
        own_occ = pos.white_occ
    else:
        bishops = pos.pieces[PIECE_TO_INDEX["b"]]
        own_occ = pos.black_occ

    bb = bishops
    while bb:
        from_sq, bb = pop_lsb(bb)
        attacks = bishop_attacks(from_sq, pos.all_occ)
        targets = attacks & ~own_occ

        t = targets
        while t:
            to_sq, t = pop_lsb(t)
            moves.append(Move(from_sq, to_sq))

    return moves

def generate_queen_moves(pos: Position) -> list[Move]:
    moves: list[Move] = []

    if pos.side_to_move == "w":
        queens = pos.pieces[PIECE_TO_INDEX["Q"]]
        own_occ = pos.white_occ
    else:
        queens = pos.pieces[PIECE_TO_INDEX["q"]]
        own_occ = pos.black_occ

    bb = queens
    while bb:
        from_sq, bb = pop_lsb(bb)
        attacks = queen_attacks(from_sq, pos.all_occ)
        targets = attacks & ~own_occ

        t = targets
        while t:
            to_sq, t = pop_lsb(t)
            moves.append(Move(from_sq, to_sq))

    return moves


def generate_all_moves(pos: Position) -> list[Move]:
    """Generate all pseudo-legal moves for the current position."""
    moves: list[Move] = []
    moves.extend(generate_pawn_moves(pos))
    moves.extend(generate_knight_moves(pos))
    moves.extend(generate_bishop_moves(pos))
    moves.extend(generate_rook_moves(pos))
    moves.extend(generate_queen_moves(pos))
    moves.extend(generate_king_moves(pos))
    return moves