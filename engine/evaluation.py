from .position import PIECE_TO_INDEX, Position
from .bitboard import pop_lsb

# Piece values in centipawns (1 pawn = 100)
PIECE_VALUES = {
    "P": 100,
    "N": 320,
    "B": 330,
    "R": 500,
    "Q": 900,
    "K": 0,  # King is invaluable, doesn't count for material
    "p": 100,
    "n": 320,
    "b": 330,
    "r": 500,
    "q": 900,
    "k": 0,
}

def count_bits(bb: int) -> int:
    count = 0
    while bb:
        bb &= bb - 1  # Clear the least significant bit
        count += 1
    return count

def evaluate(pos: Position) -> int:
    """
    Evaluate the position from white's perspective.
    Positive = white is better, negative = black is better.
    Returns score in centipawns.
    """
    score = 0
    
    # Material count
    for piece, value in PIECE_VALUES.items():
        idx = PIECE_TO_INDEX[piece]
        piece_count = count_bits(pos.pieces[idx])
        
        if piece.isupper():  # White piece
            score += piece_count * value
        else:  # Black piece
            score -= piece_count * value
    
    return score