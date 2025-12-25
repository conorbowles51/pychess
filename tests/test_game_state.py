from engine.fen import parse_fen
from engine.movegen import is_in_check, is_checkmate, is_stalemate


def test_starting_position_not_in_check():
    pos = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    assert not is_in_check(pos)


def test_simple_check():
    # White king on e1, black rook on e8
    pos = parse_fen("4r3/8/8/8/8/8/8/4K3 w - - 0 1")
    assert is_in_check(pos)


def test_not_checkmate_can_escape():
    # White king on e1, black rook on e8, king can move to d1 or f1
    pos = parse_fen("4r3/8/8/8/8/8/8/4K3 w - - 0 1")
    assert is_in_check(pos)
    assert not is_checkmate(pos)


def test_back_rank_checkmate():
    # Classic back rank mate - white rook on a8 attacks black king on g8
    pos = parse_fen("R5k1/5ppp/8/8/8/8/8/4K3 b - - 0 1")
    assert is_in_check(pos)
    assert is_checkmate(pos)


def test_scholars_mate():
    # Scholar's mate position
    pos = parse_fen("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")
    assert is_in_check(pos)
    assert is_checkmate(pos)


def test_simple_stalemate():
    # Black king on a8, white king on b6, white queen on c7 - black to move
    pos = parse_fen("k7/2Q5/1K6/8/8/8/8/8 b - - 0 1")
    assert not is_in_check(pos)
    assert is_stalemate(pos)


def test_not_stalemate_has_moves():
    pos = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    assert not is_stalemate(pos)
