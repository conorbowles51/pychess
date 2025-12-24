from engine.fen import parse_fen
from engine.movegen import generate_pawn_moves

def test_white_en_passant():
    # Black has just played d7d5, so ep square is d6.
    # White pawn on e5 can capture en passant: e5d6
    pos = parse_fen("8/8/8/3pP3/8/8/8/8 w - d6 0 1")
    moves = sorted(m.to_uci() for m in generate_pawn_moves(pos))
    assert "e5d6" in moves

def test_black_en_passant():
    # White has just played e2e4, so ep square is e3.
    # Black pawn on d4 can capture en passant: d4e3
    pos = parse_fen("8/8/8/8/3p4/8/4P3/8 b - e3 0 1")
    moves = sorted(m.to_uci() for m in generate_pawn_moves(pos))
    assert "d4e3" in moves
