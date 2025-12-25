from .bitboard import square_index, set_bit
from .position import Position, PIECE_TO_INDEX

# Example fen: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

FILES = "abcdefgh"

def parse_fen(fen: str) -> Position:
    parts = fen.strip().split()
    if len(parts) != 6:
        raise ValueError("FEN must have 6 fields")
    
    placement, stm, castling, ep, halfmove, fullmove = parts
    pos = Position.empty()

    # Piece placement: 8 ranks separated with a '/'
    ranks = placement.split("/")
    if len(ranks) != 8:
        raise ValueError("FEN must have 8 ranks")
    
    for fen_rank_index, rank_str in enumerate(ranks):
        rank = 7 - fen_rank_index
        file = 0

        for ch in rank_str:
            if ch.isdigit():
                file += int(ch)
            else:
                if ch not in PIECE_TO_INDEX:
                    raise ValueError(f"Invalid piece in FEN: {ch}")
                if file > 7:
                    raise ValueError("Too many files in rank")
                
                sq = square_index(file, rank)
                idx = PIECE_TO_INDEX[ch]
                pos.pieces[idx] = set_bit(pos.pieces[idx], sq)
                file += 1
        
        if file != 8:
            raise ValueError("Rank does not sum to 8 squares")
    
    if stm not in ("w", "b"):
        raise ValueError("Side to move must be w or b")

    pos.side_to_move = stm
    pos.castling = castling

    if ep == "-":
        pos.ep_square = None
    else:
        f = FILES.index(ep[0])
        r = int(ep[1]) - 1
        pos.ep_square = square_index(f, r)

    pos.halfmove_clock = int(halfmove)
    pos.fullmove_number = int(fullmove)

    pos.recompute_occupancy()
    return pos        