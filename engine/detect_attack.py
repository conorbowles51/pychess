from .position import Position, PIECE_TO_INDEX
from .attacks import KNIGHT_ATTACKS, KING_ATTACKS
from .sliders import rook_attacks, bishop_attacks

def is_square_attacked(pos: Position, sq: int, by_side: str) -> bool:
    if by_side == "w":
        pawns = pos.pieces[PIECE_TO_INDEX["P"]]
        knights = pos.pieces[PIECE_TO_INDEX["N"]]
        bishops = pos.pieces[PIECE_TO_INDEX["B"]]
        rooks = pos.pieces[PIECE_TO_INDEX["R"]]
        queens = pos.pieces[PIECE_TO_INDEX["Q"]]
        king = pos.pieces[PIECE_TO_INDEX["K"]]
    else:
        pawns = pos.pieces[PIECE_TO_INDEX["p"]]
        knights = pos.pieces[PIECE_TO_INDEX["n"]]
        bishops = pos.pieces[PIECE_TO_INDEX["b"]]
        rooks = pos.pieces[PIECE_TO_INDEX["r"]]
        queens = pos.pieces[PIECE_TO_INDEX["q"]]
        king = pos.pieces[PIECE_TO_INDEX["k"]]

    if KNIGHT_ATTACKS[sq] & knights:
        return True
    
    if KING_ATTACKS[sq] & king:
        return True
    
    if rook_attacks(sq, pos.all_occ) & (rooks | queens):
        return True
    
    if bishop_attacks(sq, pos.all_occ) & (bishops | queens):
        return True
    
    # Pawn attacks
    if by_side == "w":
        # White pawns attack upward, so they attack sq from below-left and below-right
        # If sq is attacked by white pawn, the pawn is on sq-7 or sq-9
        attackers = 0
        if sq >= 9 and (sq % 8) != 0:  # Not on a-file, can be attacked from left
            attackers |= 1 << (sq - 9)
        if sq >= 7 and (sq % 8) != 7:  # Not on h-file, can be attacked from right
            attackers |= 1 << (sq - 7)
        if pawns & attackers:
            return True
    else:
        # Black pawns attack downward, so they attack sq from above-left and above-right
        attackers = 0
        if sq <= 54 and (sq % 8) != 7:  # Not on h-file
            attackers |= 1 << (sq + 9)
        if sq <= 56 and (sq % 8) != 0:  # Not on a-file
            attackers |= 1 << (sq + 7)
        if pawns & attackers:
            return True

    return False