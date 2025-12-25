from .makeunmake import make_move
from .move import Move
from .position import Position, PIECE_TO_INDEX
from .bitboard import pop_lsb
from .detect_attack import is_square_attacked

def is_legal(pos: Position, move: Move):
    new_pos = make_move(pos, move)

    my_king_bb = new_pos.pieces[PIECE_TO_INDEX["K"]] if pos.side_to_move == "w" else new_pos.pieces[PIECE_TO_INDEX["k"]]
    my_king_sq, _  = pop_lsb(my_king_bb)

    attacking_side = "w" if pos.side_to_move == "b" else "b"
    if is_square_attacked(new_pos, my_king_sq, attacking_side):
        return False
    
    return True
