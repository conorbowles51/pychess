from engine.fen import parse_fen
from engine.movegen import generate_knight_moves

START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def test_start_position_knights():
    pos = parse_fen(START)
    moves = sorted(m.to_uci() for m in generate_knight_moves(pos))
    # White knights from b1 and g1
    assert moves == ["b1a3", "b1c3", "g1f3", "g1h3"]
