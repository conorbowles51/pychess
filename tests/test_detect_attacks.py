from engine.fen import parse_fen
from engine.detect_attack import is_square_attacked
from engine.bitboard import uci_to_sq


def test_knight_attacks_square():
    pos = parse_fen("8/8/8/8/4N3/8/8/8 w - - 0 1")
    # Knight on e4 attacks d2, f2, c3, g3, c5, g5, d6, f6
    assert is_square_attacked(pos, uci_to_sq("d6"), "w")
    assert is_square_attacked(pos, uci_to_sq("f6"), "w")
    assert is_square_attacked(pos, uci_to_sq("g5"), "w")
    assert not is_square_attacked(pos, uci_to_sq("e5"), "w")


def test_rook_attacks_square():
    pos = parse_fen("8/8/8/8/4R3/8/8/8 w - - 0 1")
    # Rook on e4 attacks e-file and 4th rank
    assert is_square_attacked(pos, uci_to_sq("e8"), "w")
    assert is_square_attacked(pos, uci_to_sq("a4"), "w")
    assert not is_square_attacked(pos, uci_to_sq("d5"), "w")


def test_rook_blocked():
    pos = parse_fen("8/8/4p3/8/4R3/8/8/8 w - - 0 1")
    # Rook on e4, blocked by pawn on e6
    assert is_square_attacked(pos, uci_to_sq("e6"), "w")  # Can attack the blocker
    assert not is_square_attacked(pos, uci_to_sq("e7"), "w")  # Can't attack past it


def test_bishop_attacks_square():
    pos = parse_fen("8/8/8/8/4B3/8/8/8 w - - 0 1")
    # Bishop on e4 attacks diagonals
    assert is_square_attacked(pos, uci_to_sq("h7"), "w")
    assert is_square_attacked(pos, uci_to_sq("b1"), "w")
    assert not is_square_attacked(pos, uci_to_sq("e5"), "w")


def test_queen_attacks_square():
    pos = parse_fen("8/8/8/8/4Q3/8/8/8 w - - 0 1")
    # Queen attacks like rook + bishop
    assert is_square_attacked(pos, uci_to_sq("e8"), "w")  # Rook-like
    assert is_square_attacked(pos, uci_to_sq("h7"), "w")  # Bishop-like
    assert not is_square_attacked(pos, uci_to_sq("d6"), "w")


def test_king_attacks_square():
    pos = parse_fen("8/8/8/8/4K3/8/8/8 w - - 0 1")
    # King on e4 attacks adjacent squares
    assert is_square_attacked(pos, uci_to_sq("e5"), "w")
    assert is_square_attacked(pos, uci_to_sq("d3"), "w")
    assert not is_square_attacked(pos, uci_to_sq("e6"), "w")


def test_white_pawn_attacks():
    pos = parse_fen("8/8/8/8/4P3/8/8/8 w - - 0 1")
    # White pawn on e4 attacks d5 and f5
    assert is_square_attacked(pos, uci_to_sq("d5"), "w")
    assert is_square_attacked(pos, uci_to_sq("f5"), "w")
    assert not is_square_attacked(pos, uci_to_sq("e5"), "w")  # Pawns don't attack forward


def test_black_pawn_attacks():
    pos = parse_fen("8/8/8/4p3/8/8/8/8 b - - 0 1")
    # Black pawn on e5 attacks d4 and f4
    assert is_square_attacked(pos, uci_to_sq("d4"), "b")
    assert is_square_attacked(pos, uci_to_sq("f4"), "b")
    assert not is_square_attacked(pos, uci_to_sq("e4"), "b")


def test_pawn_edge_of_board():
    # White pawn on a4 - should only attack b5, not wrap around
    pos = parse_fen("8/8/8/8/P7/8/8/8 w - - 0 1")
    assert is_square_attacked(pos, uci_to_sq("b5"), "w")
    assert not is_square_attacked(pos, uci_to_sq("h5"), "w")  # No wraparound!


def test_king_in_check_by_knight():
    pos = parse_fen("8/8/5n2/8/4K3/8/8/8 w - - 0 1")
    # White king on e4, black knight on f6 attacks it
    assert is_square_attacked(pos, uci_to_sq("e4"), "b")


def test_king_not_in_check():
    pos = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    # Starting position - white king on e1 is not attacked
    assert not is_square_attacked(pos, uci_to_sq("e1"), "b")


def test_multiple_attackers():
    pos = parse_fen("8/8/4r3/8/2r1K3/8/8/8 w - - 0 1")
    # White king on e4, attacked by rooks on c4 and e6
    assert is_square_attacked(pos, uci_to_sq("e4"), "b")
