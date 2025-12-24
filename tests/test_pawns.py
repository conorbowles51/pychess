from engine.fen import parse_fen
from engine.movegen import generate_pawn_moves

def test_start_position_white_pawn_pushes():
    pos = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    moves = sorted(m.to_uci() for m in generate_pawn_moves(pos))

    # from start position, white has 16 pawn pushes (8 single, 8 double)
    assert len(moves) == 16
    assert "a2a3" in moves and "a2a4" in moves
    assert "e2e3" in moves and "e2e4" in moves

def test_white_pawn_captures():
    # White pawn on d4 can capture c5 and e5 if black pieces there
    pos = parse_fen("8/8/8/2ppp3/3P4/8/8/8 w - - 0 1")
    moves = sorted(m.to_uci() for m in generate_pawn_moves(pos))
    assert moves == ["d4c5", "d4e5"]

def test_black_pawn_pushes_and_captures():
    pos = parse_fen("8/8/8/3p4/4P3/8/8/8 b - - 0 1")
    moves = sorted(m.to_uci() for m in generate_pawn_moves(pos))
    # black pawn on d5 can capture e4 (white pawn)
    assert "d5e4" in moves
