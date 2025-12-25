from engine.fen import parse_fen
from engine.makeunmake import make_move
from engine.move import Move
from engine.bitboard import is_set, uci_to_sq
from engine.position import PIECE_TO_INDEX

def test_simple_pawn_push():
    pos = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    move = Move(uci_to_sq("e2"), uci_to_sq("e4"))
    new_pos = make_move(pos, move)
    
    # Pawn should be on e4, not e2
    assert not is_set(new_pos.pieces[PIECE_TO_INDEX["P"]], uci_to_sq("e2"))
    assert is_set(new_pos.pieces[PIECE_TO_INDEX["P"]], uci_to_sq("e4"))
    # Side to move should switch
    assert new_pos.side_to_move == "b"
    # En passant square should be set
    assert new_pos.ep_square == uci_to_sq("e3")

def test_capture():
    pos = parse_fen("8/8/8/3p4/4P3/8/8/8 w - - 0 1")
    move = Move(uci_to_sq("e4"), uci_to_sq("d5"))
    new_pos = make_move(pos, move)
    
    # White pawn should be on d5
    assert is_set(new_pos.pieces[PIECE_TO_INDEX["P"]], uci_to_sq("d5"))
    # Black pawn should be gone
    assert not is_set(new_pos.pieces[PIECE_TO_INDEX["p"]], uci_to_sq("d5"))
    # Halfmove clock should reset on capture
    assert new_pos.halfmove_clock == 0

def test_en_passant_capture():
    # White pawn on e5, black just played d7d5
    pos = parse_fen("8/8/8/3pP3/8/8/8/8 w - d6 0 1")
    move = Move(uci_to_sq("e5"), uci_to_sq("d6"))
    new_pos = make_move(pos, move)
    
    # White pawn should be on d6
    assert is_set(new_pos.pieces[PIECE_TO_INDEX["P"]], uci_to_sq("d6"))
    # Black pawn on d5 should be captured
    assert not is_set(new_pos.pieces[PIECE_TO_INDEX["p"]], uci_to_sq("d5"))

def test_promotion():
    pos = parse_fen("8/4P3/8/8/8/8/8/8 w - - 0 1")
    move = Move(uci_to_sq("e7"), uci_to_sq("e8"), "q")
    new_pos = make_move(pos, move)
    
    # Pawn should be gone
    assert not is_set(new_pos.pieces[PIECE_TO_INDEX["P"]], uci_to_sq("e8"))
    # Queen should be on e8
    assert is_set(new_pos.pieces[PIECE_TO_INDEX["Q"]], uci_to_sq("e8"))

def test_promotion_capture():
    pos = parse_fen("3r4/4P3/8/8/8/8/8/8 w - - 0 1")
    move = Move(uci_to_sq("e7"), uci_to_sq("d8"), "q")
    new_pos = make_move(pos, move)
    
    # Queen should be on d8
    assert is_set(new_pos.pieces[PIECE_TO_INDEX["Q"]], uci_to_sq("d8"))
    # Black rook should be captured
    assert not is_set(new_pos.pieces[PIECE_TO_INDEX["r"]], uci_to_sq("d8"))

def test_kingside_castling_white():
    pos = parse_fen("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1")
    move = Move(uci_to_sq("e1"), uci_to_sq("g1"))
    new_pos = make_move(pos, move)
    
    # King should be on g1
    assert is_set(new_pos.pieces[PIECE_TO_INDEX["K"]], uci_to_sq("g1"))
    # Rook should be on f1
    assert is_set(new_pos.pieces[PIECE_TO_INDEX["R"]], uci_to_sq("f1"))
    # Rook should not be on h1
    assert not is_set(new_pos.pieces[PIECE_TO_INDEX["R"]], uci_to_sq("h1"))
    # White castling rights should be gone
    assert "K" not in new_pos.castling
    assert "Q" not in new_pos.castling

def test_queenside_castling_white():
    pos = parse_fen("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1")
    move = Move(uci_to_sq("e1"), uci_to_sq("c1"))
    new_pos = make_move(pos, move)
    
    # King should be on c1
    assert is_set(new_pos.pieces[PIECE_TO_INDEX["K"]], uci_to_sq("c1"))
    # Rook should be on d1
    assert is_set(new_pos.pieces[PIECE_TO_INDEX["R"]], uci_to_sq("d1"))
    # Rook should not be on a1
    assert not is_set(new_pos.pieces[PIECE_TO_INDEX["R"]], uci_to_sq("a1"))

def test_kingside_castling_black():
    pos = parse_fen("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R b KQkq - 0 1")
    move = Move(uci_to_sq("e8"), uci_to_sq("g8"))
    new_pos = make_move(pos, move)
    
    # King should be on g8
    assert is_set(new_pos.pieces[PIECE_TO_INDEX["k"]], uci_to_sq("g8"))
    # Rook should be on f8
    assert is_set(new_pos.pieces[PIECE_TO_INDEX["r"]], uci_to_sq("f8"))
    # Black castling rights should be gone
    assert "k" not in new_pos.castling
    assert "q" not in new_pos.castling

def test_rook_move_removes_castling_rights():
    pos = parse_fen("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1")
    move = Move(uci_to_sq("h1"), uci_to_sq("h2"))
    new_pos = make_move(pos, move)
    
    # Kingside castling right should be gone
    assert "K" not in new_pos.castling
    # Queenside should remain
    assert "Q" in new_pos.castling

def test_rook_captured_removes_castling_rights():
    # White bishop on b7 can capture the a8 rook
    pos = parse_fen("r3k2r/pBpppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1")
    move = Move(uci_to_sq("b7"), uci_to_sq("a8"))  # Bishop captures a8 rook
    new_pos = make_move(pos, move)
    
    # Black queenside castling right should be gone
    assert "q" not in new_pos.castling

def test_halfmove_clock_increments():
    pos = parse_fen("8/8/8/8/8/5N2/8/8 w - - 5 10")
    move = Move(uci_to_sq("f3"), uci_to_sq("e5"))
    new_pos = make_move(pos, move)
    
    assert new_pos.halfmove_clock == 6

def test_halfmove_clock_resets_on_pawn_move():
    pos = parse_fen("8/8/8/8/8/8/4P3/8 w - - 5 10")
    move = Move(uci_to_sq("e2"), uci_to_sq("e4"))
    new_pos = make_move(pos, move)
    
    assert new_pos.halfmove_clock == 0

def test_fullmove_increments_after_black():
    pos = parse_fen("8/4p3/8/8/8/8/8/8 b - - 0 10")
    move = Move(uci_to_sq("e7"), uci_to_sq("e5"))
    new_pos = make_move(pos, move)
    
    assert new_pos.fullmove_number == 11

def test_fullmove_stays_after_white():
    pos = parse_fen("8/8/8/8/8/8/4P3/8 w - - 0 10")
    move = Move(uci_to_sq("e2"), uci_to_sq("e4"))
    new_pos = make_move(pos, move)
    
    assert new_pos.fullmove_number == 10

def test_ep_square_cleared_after_non_double_push():
    pos = parse_fen("8/8/8/8/8/4P3/8/8 w - e6 0 1")
    move = Move(uci_to_sq("e3"), uci_to_sq("e4"))
    new_pos = make_move(pos, move)
    
    assert new_pos.ep_square is None