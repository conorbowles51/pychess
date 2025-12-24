
# File masks with all bits set on given file
FILE_A = 0x0101010101010101
FILE_B = FILE_A << 1
FILE_G = FILE_A << 6
FILE_H = FILE_A << 7

NOT_FILE_A = ~FILE_A & 0xFFFFFFFFFFFFFFFF
NOT_FILE_H = ~FILE_H & 0xFFFFFFFFFFFFFFFF
NOT_FILE_AB = ~(FILE_A | FILE_B) & 0xFFFFFFFFFFFFFFFF
NOT_FILE_GH = ~(FILE_G | FILE_H) & 0xFFFFFFFFFFFFFFFF

# Ensures we only have 64 bits
def _mask64(x: int) -> int:
    return x & 0xFFFFFFFFFFFFFFFF

def knight_attacks_from(sq: int) -> int:
    bb = 1 << sq

    # Knight moves are +- 1 file and +- 2 ranks or vice versa
    # E.g, up up right is +8 +8 + 1 = +17

    attacks = 0

    # 2 up, 1 left or right
    attacks |= (bb & NOT_FILE_H) << 17
    attacks |= (bb & NOT_FILE_A) << 15

    # 2 down, 1 left or right
    attacks |= (bb & NOT_FILE_H) >> 15
    attacks |= (bb & NOT_FILE_A) >> 17

    # 1 up, 2 left or right
    attacks |= (bb & NOT_FILE_GH) << 10
    attacks |= (bb & NOT_FILE_AB) << 6

    # 1 down, 2 left or right
    attacks |= (bb & NOT_FILE_GH) >> 6
    attacks |= (bb & NOT_FILE_AB) >> 10

    # If a knight attach goes too high, make sure we trim it back to 64 bits with mask64
    return _mask64(attacks)

# Precompute knight attacks for every square
KNIGHT_ATTACKS = [knight_attacks_from(sq) for sq in range(64)]