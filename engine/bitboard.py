FILES = "abcdefgh"
RANKS = "12345678"

# Return index of square, a1 = 0, h8 = 63
def square_index(file: int, rank: int) -> int:
    return rank * 8 + file

# Convert 'e2' to square index
def uci_to_sq(s: str) -> int:
    file = FILES.index(s[0])
    rank = RANKS.index(s[1])
    return square_index(file, rank)

def sq_to_uci(sq: int) -> str:
    file = sq % 8
    rank = sq // 8
    return f"{FILES[file]}{RANKS[rank]}"

# Returns a mask with only that square 'on'
# I.e, if we look for square index 7 (a8)
# we get 0b000000...01 -> 0b000...100000000
def bit(sq: int) -> int:
    return 1 << sq

# ORs the bitboard and a mask
def set_bit(bb: int, sq: int) -> int:
    return bb | bit(sq)

def clear_bit(bb: int, sq: int) -> int:
    return bb & ~bit(sq)

# Moves desired sq to position 0 (least significant position)
# ANDs it with 0b00...01. If it is set, it will be 1, else 0
def is_set(bb: int, sq: int) -> bool:
    return (bb >> sq) & 1 == 1

def pop_lsb(bb: int) -> tuple[int, int]:
    # This is a bit of bit magic, hurts my brain a bit but all you need to know is
    # only the lowest set bit survives the &
    lsb = bb & -bb
    # Bit length is how many bits do we need to store lsb
    # so 0b000..1000 will be 4 bits. Subtract 1 to get 3rd position sq
    sq = lsb.bit_length() - 1
    # Exclusive OR to pop bit
    bb ^= lsb
    return sq, bb