from engine.fen import parse_fen
from engine.movegen import generate_pawn_moves

def test_white_pawn_promotion_push():
    pos = parse_fen("8/4P3/8/8/8/8/8/8 w - - 0 1")  # white pawn on e7
    moves = sorted(m.to_uci() for m in generate_pawn_moves(pos))
    assert moves == ["e7e8b", "e7e8n", "e7e8q", "e7e8r"]

def test_white_pawn_promotion_capture():
    pos = parse_fen("1rn5/1P6/8/8/8/8/8/8 w - - 0 1")  # b8 rook blocks push, c8 knight is capturable
    moves = sorted(m.to_uci() for m in generate_pawn_moves(pos))
    assert moves == ["b7c8b", "b7c8n", "b7c8q", "b7c8r"]


def test_black_pawn_promotion_push():
    pos = parse_fen("8/8/8/8/8/8/4p3/8 b - - 0 1")  # black pawn on e2
    moves = sorted(m.to_uci() for m in generate_pawn_moves(pos))
    assert moves == ["e2e1b", "e2e1n", "e2e1q", "e2e1r"]
