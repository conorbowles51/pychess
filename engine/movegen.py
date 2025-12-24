from .position import Position, PIECE_TO_INDEX
from .attacks import KNIGHT_ATTACKS
from .bitboard import pop_lsb
from .move import Move

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