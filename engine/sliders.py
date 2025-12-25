# Sliding piece attack generation (rooks, bishops, queens)

from .bitboard import bit

MASK64 = 0xFFFFFFFFFFFFFFFF

# Direction deltas for rooks
NORTH = 8
SOUTH = -8
EAST = 1
WEST = -1

# Direction deltas for bishops
NORTH_EAST = 9
NORTH_WEST = 7
SOUTH_EAST = -7
SOUTH_WEST = -9

def file_of(sq: int) -> int:
    return sq % 8

def rank_of(sq: int) -> int:
    return sq // 8


def ray_attacks(sq: int, direction: int, occupancy: int) -> int:
    attacks = 0
    current_sq = sq
    current_file = file_of(sq)
    
    while True:
        # Step in direction
        current_sq += direction
        new_file = file_of(current_sq)
        
        # Check if we've left the board (top or bottom)
        if current_sq < 0 or current_sq > 63:
            break
        
        # Check if we've wrapped around (east/west movement)
        # If we moved east (+1), file should increase by 1
        # If we moved west (-1), file should decrease by 1
        # If file changed by more than 1, we wrapped
        file_diff = abs(new_file - current_file)
        if file_diff > 1:
            break
        
        # This square is attackable
        attacks |= bit(current_sq)
        
        # If there's a piece here, we stop (can capture but not go through)
        if occupancy & bit(current_sq):
            break
        
        current_file = new_file
    
    return attacks


def rook_attacks(sq: int, occupancy: int) -> int:
    attacks = 0
    attacks |= ray_attacks(sq, NORTH, occupancy)
    attacks |= ray_attacks(sq, SOUTH, occupancy)
    attacks |= ray_attacks(sq, EAST, occupancy)
    attacks |= ray_attacks(sq, WEST, occupancy)
    return attacks


def bishop_attacks(sq: int, occupancy: int) -> int:
    attacks = 0
    attacks |= ray_attacks(sq, NORTH_EAST, occupancy)
    attacks |= ray_attacks(sq, NORTH_WEST, occupancy)
    attacks |= ray_attacks(sq, SOUTH_EAST, occupancy)
    attacks |= ray_attacks(sq, SOUTH_WEST, occupancy)
    return attacks


def queen_attacks(sq: int, occupancy: int) -> int:
    return rook_attacks(sq, occupancy) | bishop_attacks(sq, occupancy)