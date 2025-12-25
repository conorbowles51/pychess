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

# Piece-Square Tables (a1=0, h8=63)
# Written with rank 1 first, rank 8 last

PAWN_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,   # Rank 1 (no pawns here)
     5, 10, 10,-20,-20, 10, 10,  5,   # Rank 2 (start - center pawns should push)
     5, -5,-10,  0,  0,-10, -5,  5,   # Rank 3
     0,  0,  0, 20, 20,  0,  0,  0,   # Rank 4
     5,  5, 10, 25, 25, 10,  5,  5,   # Rank 5
    10, 10, 20, 30, 30, 20, 10, 10,   # Rank 6
    50, 50, 50, 50, 50, 50, 50, 50,   # Rank 7 (about to promote!)
     0,  0,  0,  0,  0,  0,  0,  0,   # Rank 8 (promoted)
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,  # Rank 1
    -40,-20,  0,  5,  5,  0,-20,-40,  # Rank 2
    -30,  5, 10, 15, 15, 10,  5,-30,  # Rank 3
    -30,  0, 15, 20, 20, 15,  0,-30,  # Rank 4
    -30,  5, 15, 20, 20, 15,  5,-30,  # Rank 5
    -30,  0, 10, 15, 15, 10,  0,-30,  # Rank 6
    -40,-20,  0,  0,  0,  0,-20,-40,  # Rank 7
    -50,-40,-30,-30,-30,-30,-40,-50,  # Rank 8
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,  # Rank 1
    -10,  5,  0,  0,  0,  0,  5,-10,  # Rank 2
    -10, 10, 10, 10, 10, 10, 10,-10,  # Rank 3
    -10,  0, 10, 10, 10, 10,  0,-10,  # Rank 4
    -10,  5,  5, 10, 10,  5,  5,-10,  # Rank 5
    -10,  0,  5, 10, 10,  5,  0,-10,  # Rank 6
    -10,  0,  0,  0,  0,  0,  0,-10,  # Rank 7
    -20,-10,-10,-10,-10,-10,-10,-20,  # Rank 8
]

ROOK_TABLE = [
     0,  0,  0,  5,  5,  0,  0,  0,   # Rank 1
    -5,  0,  0,  0,  0,  0,  0, -5,   # Rank 2
    -5,  0,  0,  0,  0,  0,  0, -5,   # Rank 3
    -5,  0,  0,  0,  0,  0,  0, -5,   # Rank 4
    -5,  0,  0,  0,  0,  0,  0, -5,   # Rank 5
    -5,  0,  0,  0,  0,  0,  0, -5,   # Rank 6
     5, 10, 10, 10, 10, 10, 10,  5,   # Rank 7 (rooks love 7th rank)
     0,  0,  0,  0,  0,  0,  0,  0,   # Rank 8
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,  # Rank 1
    -10,  0,  0,  0,  0,  0,  0,-10,  # Rank 2
    -10,  0,  5,  5,  5,  5,  0,-10,  # Rank 3
     -5,  0,  5,  5,  5,  5,  0, -5,  # Rank 4
      0,  0,  5,  5,  5,  5,  0, -5,  # Rank 5
    -10,  5,  5,  5,  5,  5,  0,-10,  # Rank 6
    -10,  0,  5,  0,  0,  0,  0,-10,  # Rank 7
    -20,-10,-10, -5, -5,-10,-10,-20,  # Rank 8
]

KING_MIDDLEGAME_TABLE = [
     20, 30, 10,  0,  0, 10, 30, 20,  # Rank 1 (castled king is safe here!)
     20, 20,  0,  0,  0,  0, 20, 20,  # Rank 2
    -10,-20,-20,-20,-20,-20,-20,-10,  # Rank 3
    -20,-30,-30,-40,-40,-30,-30,-20,  # Rank 4
    -30,-40,-40,-50,-50,-40,-40,-30,  # Rank 5
    -30,-40,-40,-50,-50,-40,-40,-30,  # Rank 6
    -30,-40,-40,-50,-50,-40,-40,-30,  # Rank 7
    -30,-40,-40,-50,-50,-40,-40,-30,  # Rank 8
]

def count_bits(bb: int) -> int:
    count = 0
    while bb:
        bb &= bb - 1  # Clear the least significant bit
        count += 1
    return count

def flip_square(sq: int) -> int:
    """Flip square vertically for black's perspective."""
    # a1 (0) -> a8 (56), h1 (7) -> h8 (63), etc.
    rank = sq // 8
    file = sq % 8
    return (7 - rank) * 8 + file

def evaluate(pos: Position) -> int:
    """
    Evaluate the position from white's perspective.
    Positive = white is better, negative = black is better.
    Returns score in centipawns.
    """
    score = 0
    
    # For each piece type, count material and add positional bonus
    for piece, value in PIECE_VALUES.items():
        idx = PIECE_TO_INDEX[piece]
        bb = pos.pieces[idx]
        
        # Get the appropriate table
        if piece.lower() == 'p':
            table = PAWN_TABLE
        elif piece.lower() == 'n':
            table = KNIGHT_TABLE
        elif piece.lower() == 'b':
            table = BISHOP_TABLE
        elif piece.lower() == 'r':
            table = ROOK_TABLE
        elif piece.lower() == 'q':
            table = QUEEN_TABLE
        elif piece.lower() == 'k':
            table = KING_MIDDLEGAME_TABLE
        
        # Loop through each piece of this type
        while bb:
            sq = (bb & -bb).bit_length() - 1  # Get LSB square
            bb &= bb - 1  # Clear LSB
            
            if piece.isupper():  # White
                score += value + table[sq]
            else:  # Black
                score -= value + table[flip_square(sq)]
    
    return score