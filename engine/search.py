from .position import Position
from .movegen import generate_legal_moves, is_in_check, generate_captures
from .makeunmake import make_move
from .evaluation import evaluate
from .move import Move
from .move_validator import is_legal
from .zobrist import hash_position

INFINITY = 999_999
CHECKMATE_SCORE = 100_000

# Piece values for move ordering (simpler than evaluation values)
MVV_LVA_VICTIM = [100, 320, 330, 500, 900, 10000, 100, 320, 330, 500, 900, 10000]

def get_piece_at(pos: Position, sq: int) -> int | None:
    """Return piece index at square, or None if empty."""
    mask = 1 << sq
    for i in range(12):
        if pos.pieces[i] & mask:
            return i
    return None


def score_move(pos: Position, move: Move) -> int:
    """Score a move for ordering. Higher = search first."""
    score = 0
    
    # Captures: MVV-LVA
    victim = get_piece_at(pos, move.to_sq)
    if victim is not None:
        attacker = get_piece_at(pos, move.from_sq)
        if attacker is not None:
            score += 10000 + MVV_LVA_VICTIM[victim] - MVV_LVA_VICTIM[attacker] // 100
    
    # Promotions are good
    if move.promo:
        score += 9000
    
    return score


def order_moves(pos: Position, moves: list[Move]) -> list[Move]:
    """Order moves: captures and promotions first."""
    return sorted(moves, key=lambda m: score_move(pos, m), reverse=True)

def quiescence(pos: Position, alpha: int, beta: int) -> int:
    """
    Search captures until the position is quiet.
    """
    stand_pat = evaluate(pos)
    if pos.side_to_move == "b":
        stand_pat = -stand_pat
    
    if stand_pat >= beta:
        return beta
    
    if stand_pat > alpha:
        alpha = stand_pat
    
    captures = generate_captures(pos)
    captures = order_moves(pos, captures)  # Order captures too!
    
    for move in captures:
        if not is_legal(pos, move):
            continue
            
        new_pos = make_move(pos, move)
        score = -quiescence(new_pos, -beta, -alpha)
        
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    
    return alpha

def negamax(pos: Position, depth: int, alpha: int, beta: int, history: set[int]) -> int:
    """
    Negamax search with alpha-beta pruning.
    """
    pos_hash = hash_position(pos)
    if pos_hash in history:
        return 0
    
    if depth == 0:
        return quiescence(pos, alpha, beta)
    
    moves = generate_legal_moves(pos)
    
    if not moves:
        if is_in_check(pos):
            return -CHECKMATE_SCORE
        return 0
    
    # Order moves for better pruning
    moves = order_moves(pos, moves)
    
    new_history = history | {pos_hash}
    
    for move in moves:
        new_pos = make_move(pos, move)
        score = -negamax(new_pos, depth - 1, -beta, -alpha, new_history)
        
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    
    return alpha


def search(pos: Position, depth: int, history: set[int] | None = None) -> tuple[Move | None, int]:
    """
    Search for the best move.
    """
    if history is None:
        history = set()
    
    best_move = None
    alpha = -INFINITY
    beta = INFINITY
    
    moves = generate_legal_moves(pos)
    
    if not moves:
        return None, 0
    
    # Order moves
    moves = order_moves(pos, moves)
    
    pos_hash = hash_position(pos)
    new_history = history | {pos_hash}
    
    for move in moves:
        new_pos = make_move(pos, move)
        score = -negamax(new_pos, depth - 1, -beta, -alpha, new_history)
        
        if score > alpha:
            alpha = score
            best_move = move
    
    print(f"info depth {depth} score cp {alpha}")
    
    return best_move, alpha