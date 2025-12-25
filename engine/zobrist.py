import random

# Fix the seed so hashes are consistent across runs
random.seed(1234567)

# Random number for each piece on each square (12 pieces x 64 squares)
PIECE_KEYS = [[random.getrandbits(64) for _ in range(64)] for _ in range(12)]

# Random number for side to move
SIDE_KEY = random.getrandbits(64)

# Random numbers for castling rights (4 bits = 16 combinations)
CASTLING_KEYS = [random.getrandbits(64) for _ in range(16)]

# Random numbers for en passant file (8 files + 1 for no ep)
EP_KEYS = [random.getrandbits(64) for _ in range(9)]


def castling_to_index(castling: str) -> int:
    """Convert castling string to index 0-15."""
    idx = 0
    if 'K' in castling: idx |= 1
    if 'Q' in castling: idx |= 2
    if 'k' in castling: idx |= 4
    if 'q' in castling: idx |= 8
    return idx


def hash_position(pos) -> int:
    """Generate a Zobrist hash for the position."""
    h = 0
    
    # Hash pieces
    for piece_idx in range(12):
        bb = pos.pieces[piece_idx]
        while bb:
            sq = (bb & -bb).bit_length() - 1
            bb &= bb - 1
            h ^= PIECE_KEYS[piece_idx][sq]
    
    # Hash side to move
    if pos.side_to_move == "b":
        h ^= SIDE_KEY
    
    # Hash castling rights
    h ^= CASTLING_KEYS[castling_to_index(pos.castling)]
    
    # Hash en passant
    if pos.ep_square is not None:
        ep_file = pos.ep_square % 8
        h ^= EP_KEYS[ep_file]
    else:
        h ^= EP_KEYS[8]  # No ep
    
    return h