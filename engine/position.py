from dataclasses import dataclass

# There are 12 bitboards per position: one per piece type per color
# White: P N B R Q K
# Black: p n b r q k

PIECE_ORDER = "PNBRQKpnbrqk"
PIECE_TO_INDEX = {p: i for i, p in enumerate(PIECE_ORDER)}

@dataclass(slots=True)
class Position:
    # 12 piece bitboards in order of PIECE_ORDER
    pieces: list[int]

    # Convienience occupancy boards, derived but cached
    white_occ: int
    black_occ: int
    all_occ: int

    # Game state
    side_to_move: str       # "w" or "b"
    castling: str           # "KQkq" or "-" (matches FEN way of storing castling rights)
    ep_square: int | None   # En passant square, if applicable
    halfmove_clock: int     # Half move is one side only (black move or white move). Exists for 50 move rule
    fullmove_number: int    # Move number

    @staticmethod
    def empty() -> "Position":
        return Position(
            pieces=[0] * 12,
            white_occ=0,
            black_occ=0,
            all_occ=0,
            side_to_move="w",
            castling="-",
            ep_square=None,
            halfmove_clock=0,
            fullmove_number=1,
        )
    
    def recompute_occupancy(self) -> None:
        w = 0
        b = 0
        for i in range(6):
            w |= self.pieces[i]
        for i in range(6, 12):
            b |= self.pieces[i]
        self.white_occ = w
        self.black_occ = b
        self.all_occ = w | b

    def copy(self) -> "Position":
        return Position(
            self.pieces.copy(),
            self.white_occ,
            self.black_occ,
            self.all_occ,
            self.side_to_move,
            self.castling,
            self.ep_square,
            self.halfmove_clock,
            self.fullmove_number
        )

# Pretty print for debugging
def pretty(pos: Position) -> str:
    board = ["." for _ in range(64)]
    # Fill squares by scanning bitboards
    for piece_char, idx in PIECE_TO_INDEX.items():
        bb = pos.pieces[idx]
        while bb:
            lsb = bb & -bb
            sq = lsb.bit_length() - 1
            board[sq] = piece_char
            bb ^= lsb
    lines = []
    for rank in range(7, -1, -1):
        row = board[rank * 8 : rank * 8 + 8]
        lines.append(f"{rank+1}  " + " ".join(row))
    lines.append("   a b c d e f g h")
    return "\n".join(lines)
