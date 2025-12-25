from engine.fen import parse_fen
from engine.move import Move
from engine.bitboard import uci_to_sq
from engine.move_validator import is_legal


def test_normal_move_is_legal():
    pos = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    move = Move(uci_to_sq("e2"), uci_to_sq("e4"))
    assert is_legal(pos, move)


def test_moving_pinned_piece_is_illegal():
    # White bishop on e2 is pinned by black rook on e8
    pos = parse_fen("4r3/8/8/8/8/8/4B3/4K3 w - - 0 1")
    move = Move(uci_to_sq("e2"), uci_to_sq("d3"))  # Bishop moves off the pin
    assert not is_legal(pos, move)


def test_pinned_piece_can_move_along_pin():
    # White rook on e2 is pinned by black rook on e8, but can move along the file
    pos = parse_fen("4r3/8/8/8/8/8/4R3/4K3 w - - 0 1")
    move = Move(uci_to_sq("e2"), uci_to_sq("e5"))  # Rook moves along pin line
    assert is_legal(pos, move)


def test_king_cannot_move_into_check():
    pos = parse_fen("8/8/8/8/4r3/8/8/4K3 w - - 0 1")
    move = Move(uci_to_sq("e1"), uci_to_sq("e2"))  # King walks into rook's line
    assert not is_legal(pos, move)


def test_king_can_escape_check():
    pos = parse_fen("8/8/8/8/4r3/8/8/4K3 w - - 0 1")
    move = Move(uci_to_sq("e1"), uci_to_sq("f1"))  # King escapes sideways
    assert is_legal(pos, move)


def test_must_block_check():
    # King in check by rook, bishop can block
    pos = parse_fen("4r3/8/8/8/8/8/4B3/4K3 w - - 0 1")
    move = Move(uci_to_sq("e2"), uci_to_sq("e4"))  # Bishop blocks
    assert is_legal(pos, move)


def test_capturing_attacker_is_legal():
    # King in check by knight, queen can capture it
    pos = parse_fen("8/8/5n2/8/8/8/4Q3/4K3 w - - 0 1")
    move = Move(uci_to_sq("e2"), uci_to_sq("f6"))  # Queen captures knight
    assert is_legal(pos, move)


def test_king_cannot_capture_defended_piece():
    # Black rook on e2 defended by rook on e8
    pos = parse_fen("4r3/8/8/8/8/8/4r3/4K3 w - - 0 1")
    move = Move(uci_to_sq("e1"), uci_to_sq("e2"))  # King captures but still in check
    assert not is_legal(pos, move)