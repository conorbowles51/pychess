from engine.fen import parse_fen
from engine.movegen import generate_king_moves


def test_white_kingside_castling():
    pos = parse_fen("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1")
    moves = [m.to_uci() for m in generate_king_moves(pos)]
    assert "e1g1" in moves


def test_white_queenside_castling():
    pos = parse_fen("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1")
    moves = [m.to_uci() for m in generate_king_moves(pos)]
    assert "e1c1" in moves


def test_black_kingside_castling():
    pos = parse_fen("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R b KQkq - 0 1")
    moves = [m.to_uci() for m in generate_king_moves(pos)]
    assert "e8g8" in moves


def test_black_queenside_castling():
    pos = parse_fen("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R b KQkq - 0 1")
    moves = [m.to_uci() for m in generate_king_moves(pos)]
    assert "e8c8" in moves


def test_cannot_castle_without_rights():
    pos = parse_fen("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w - - 0 1")
    moves = [m.to_uci() for m in generate_king_moves(pos)]
    assert "e1g1" not in moves
    assert "e1c1" not in moves


def test_cannot_castle_when_blocked():
    # Knight on g1 blocks kingside castling
    pos = parse_fen("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K1NR w KQkq - 0 1")
    moves = [m.to_uci() for m in generate_king_moves(pos)]
    assert "e1g1" not in moves


def test_cannot_castle_out_of_check():
    # White king in check from black rook
    pos = parse_fen("4r3/8/8/8/8/8/8/R3K2R w KQ - 0 1")
    moves = [m.to_uci() for m in generate_king_moves(pos)]
    assert "e1g1" not in moves
    assert "e1c1" not in moves


def test_cannot_castle_through_check():
    # Black rook attacks f1, can't castle kingside
    pos = parse_fen("5r2/8/8/8/8/8/8/R3K2R w KQ - 0 1")
    moves = [m.to_uci() for m in generate_king_moves(pos)]
    assert "e1g1" not in moves
    # Q