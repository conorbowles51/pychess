from .position import Position, PIECE_TO_INDEX
from .bitboard import set_bit, clear_bit, is_set
from .move import Move

def make_move(pos: Position, move: Move) -> Position:
    new_pos = pos.copy()

    my_pieces = range(0, 6) if pos.side_to_move == "w" else range(6, 12)
    enemy_pieces = range(6, 12) if pos.side_to_move == "w" else range(0, 6)

    # Find which piece is moving
    moving_piece_idx = None
    for i in my_pieces:
        if is_set(new_pos.pieces[i], move.from_sq):
            moving_piece_idx = i
            break

    # Move our piece
    new_pos.pieces[moving_piece_idx] = clear_bit(new_pos.pieces[moving_piece_idx], move.from_sq)
    new_pos.pieces[moving_piece_idx] = set_bit(new_pos.pieces[moving_piece_idx], move.to_sq)

    # Remove captured piece (if any)
    for i in enemy_pieces:
        if is_set(new_pos.pieces[i], move.to_sq):
            new_pos.pieces[i] = clear_bit(new_pos.pieces[i], move.to_sq)
            break

    # --- Promotions ---
    if move.promo:
        # Remove the pawn we just placed on to_sq
        new_pos.pieces[moving_piece_idx] = clear_bit(new_pos.pieces[moving_piece_idx], move.to_sq)
        # Add the promoted piece
        promo_char = move.promo.upper() if pos.side_to_move == "w" else move.promo.lower()
        promo_idx = PIECE_TO_INDEX[promo_char]
        new_pos.pieces[promo_idx] = set_bit(new_pos.pieces[promo_idx], move.to_sq)

    # --- En passant capture ---
    # If a pawn moves to the ep_square, remove the captured pawn
    if pos.ep_square is not None and move.to_sq == pos.ep_square:
        # Check if it's a pawn moving (idx 0 for white P, idx 6 for black p)
        pawn_idx = 0 if pos.side_to_move == "w" else 6
        if moving_piece_idx == pawn_idx:
            # The captured pawn is one rank behind the ep_square
            if pos.side_to_move == "w":
                captured_sq = pos.ep_square - 8  # Black pawn is below ep square
                new_pos.pieces[6] = clear_bit(new_pos.pieces[6], captured_sq)  # Remove black pawn
            else:
                captured_sq = pos.ep_square + 8  # White pawn is above ep square
                new_pos.pieces[0] = clear_bit(new_pos.pieces[0], captured_sq)  # Remove white pawn

    # --- Update en passant square ---
    # Set ep_square if a pawn moved two squares
    pawn_idx = 0 if pos.side_to_move == "w" else 6
    if moving_piece_idx == pawn_idx:
        if pos.side_to_move == "w" and move.to_sq - move.from_sq == 16:
            new_pos.ep_square = move.from_sq + 8
        elif pos.side_to_move == "b" and move.from_sq - move.to_sq == 16:
            new_pos.ep_square = move.from_sq - 8
        else:
            new_pos.ep_square = None
    else:
        new_pos.ep_square = None

    # --- Castling ---
    king_idx = 5 if pos.side_to_move == "w" else 11
    if moving_piece_idx == king_idx:
        # Kingside castling
        if move.to_sq - move.from_sq == 2:
            rook_idx = 3 if pos.side_to_move == "w" else 9
            rook_from = move.from_sq + 3  # h1 or h8
            rook_to = move.from_sq + 1    # f1 or f8
            new_pos.pieces[rook_idx] = clear_bit(new_pos.pieces[rook_idx], rook_from)
            new_pos.pieces[rook_idx] = set_bit(new_pos.pieces[rook_idx], rook_to)
        # Queenside castling
        elif move.from_sq - move.to_sq == 2:
            rook_idx = 3 if pos.side_to_move == "w" else 9
            rook_from = move.from_sq - 4  # a1 or a8
            rook_to = move.from_sq - 1    # d1 or d8
            new_pos.pieces[rook_idx] = clear_bit(new_pos.pieces[rook_idx], rook_from)
            new_pos.pieces[rook_idx] = set_bit(new_pos.pieces[rook_idx], rook_to)

    # --- Update castling rights ---
    # Remove rights if king or rook moves
    new_castling = new_pos.castling
    if pos.side_to_move == "w":
        if moving_piece_idx == 5:  # King moved
            new_castling = new_castling.replace("K", "").replace("Q", "")
        if move.from_sq == 0:  # a1 rook
            new_castling = new_castling.replace("Q", "")
        if move.from_sq == 7:  # h1 rook
            new_castling = new_castling.replace("K", "")
    else:
        if moving_piece_idx == 11:  # King moved
            new_castling = new_castling.replace("k", "").replace("q", "")
        if move.from_sq == 56:  # a8 rook
            new_castling = new_castling.replace("q", "")
        if move.from_sq == 63:  # h8 rook
            new_castling = new_castling.replace("k", "")
    # Also remove rights if rook is captured
    if move.to_sq == 0:
        new_castling = new_castling.replace("Q", "")
    if move.to_sq == 7:
        new_castling = new_castling.replace("K", "")
    if move.to_sq == 56:
        new_castling = new_castling.replace("q", "")
    if move.to_sq == 63:
        new_castling = new_castling.replace("k", "")
    new_pos.castling = new_castling if new_castling else "-"

    # --- Update clocks ---
    # Halfmove clock resets on pawn move or capture
    is_capture = any(is_set(pos.pieces[i], move.to_sq) for i in enemy_pieces)
    is_pawn_move = moving_piece_idx == 0 or moving_piece_idx == 6
    if is_pawn_move or is_capture:
        new_pos.halfmove_clock = 0
    else:
        new_pos.halfmove_clock += 1

    # Fullmove number increments after black moves
    if pos.side_to_move == "b":
        new_pos.fullmove_number += 1

    # Switch side to move
    new_pos.side_to_move = "b" if pos.side_to_move == "w" else "w"

    # Recompute occupancy bitboards
    new_pos.recompute_occupancy()

    return new_pos