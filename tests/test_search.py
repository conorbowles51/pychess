from engine.fen import parse_fen
from engine.search import search


def test_search_returns_a_move():
    pos = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    move, score = search(pos, 1)
    assert move is not None


def test_search_finds_free_piece():
    # White queen can take undefended black rook
    pos = parse_fen("r3k3/8/8/8/8/8/8/4K2Q w - - 0 1")
    move, score = search(pos, 1)
    assert move.to_uci() == "h1a8"


def test_search_avoids_losing_queen():
    # White queen is attacked by black rook, must move
    pos = parse_fen("r7/8/8/8/8/8/8/Q3K3 w - - 0 1")
    move, score = search(pos, 2)
    # Queen should move off the a-file
    assert move.to_uci().startswith("a1")


def test_search_black_to_move():
    # Black queen can take undefended white rook
    pos = parse_fen("4k2q/8/8/8/8/8/8/R3K3 b - - 0 1")
    move, score = search(pos, 1)
    assert move.to_uci() == "h8a1"


def test_search_no_legal_moves():
    # Stalemate position - black has no moves
    pos = parse_fen("k7/2Q5/1K6/8/8/8/8/8 b - - 0 1")
    move, score = search(pos, 1)
    assert move is None
    assert score == 0