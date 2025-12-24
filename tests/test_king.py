from engine.fen import parse_fen
from engine.movegen import generate_king_moves

def test_king_center_has_8_moves():
    pos = parse_fen("8/8/8/3K4/8/8/8/8 w - - 0 1")  # King on d5
    moves = sorted(m.to_uci() for m in generate_king_moves(pos))
    assert len(moves) == 8
    assert moves == [
        "d5c4", "d5c5", "d5c6",
        "d5d4",         "d5d6",
        "d5e4", "d5e5", "d5e6",
    ]
