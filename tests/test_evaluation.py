from engine.fen import parse_fen
from engine.evaluation import evaluate


def test_starting_position_is_equal():
    pos = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    assert evaluate(pos) == 0


def test_white_up_a_pawn():
    # White has an extra pawn
    pos = parse_fen("rnbqkbnr/ppppppp1/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    assert evaluate(pos) == 100


def test_black_up_a_pawn():
    pos = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPP1/RNBQKBNR w KQkq - 0 1")
    assert evaluate(pos) == -100


def test_white_up_a_queen():
    # Black is missing their queen
    pos = parse_fen("rnb1kbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    assert evaluate(pos) == 900


def test_white_up_rook_for_knight():
    # White has rook, black has knight (exchange)
    pos = parse_fen("4k3/8/8/8/8/8/8/R3K3 w - - 0 1")
    white_score = 500  # rook
    black_score = 0
    assert evaluate(pos) == white_score - black_score


def test_complex_position():
    # White: K, Q, R, B, N, 3P = 0 + 900 + 500 + 330 + 320 + 300 = 2350
    # Black: K, R, R, N, 4P = 0 + 500 + 500 + 320 + 400 = 1720
    # Diff = 2350 - 1720 = 630
    pos = parse_fen("r3k2r/pppp4/8/8/8/8/PPP5/RNBQK3 w Qq - 0 1")
    score = evaluate(pos)
    # White: R(500) + N(320) + B(330) + Q(900) + K(0) + 3P(300) = 2350
    # Black: R(500) + R(500) + K(0) + 4P(400) = 1400
    assert score == 2350 - 1400


def test_only_kings():
    pos = parse_fen("4k3/8/8/8/8/8/8/4K3 w - - 0 1")
    assert evaluate(pos) == 0