from .position import Position
from .movegen import generate_legal_moves, is_in_check, generate_captures
from .makeunmake import make_move
from .evaluation import evaluate
from .move import Move
from .move_validator import is_legal
from .zobrist import hash_position

INFINITY = 999_999
CHECKMATE_SCORE = 100_000

def quiescence(pos: Position, alpha: int, beta: int) -> int:
    """
    Search captures until the position is quiet.
    Avoids evaluating in the middle of a capture sequence.
    """
    # Stand pat: evaluate current position
    # If we choose not to capture, what's our score?
    stand_pat = evaluate(pos)
    if pos.side_to_move == "b":
        stand_pat = -stand_pat
    
    # If we're already doing great, opponent won't let us get here
    if stand_pat >= beta:
        return beta
    
    # Update alpha if standing pat is good
    if stand_pat > alpha:
        alpha = stand_pat
    
    # Search captures only
    captures = generate_captures(pos)
    
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
    pos_hash = hash_position(pos)
    if pos_hash in history:
        return 0  # Draw by repetition
    
    if depth == 0:
        return quiescence(pos, alpha, beta)
    
    moves = generate_legal_moves(pos)

    if not moves:
        if is_in_check(pos):
            return -CHECKMATE_SCORE # Checkmate
        return 0 # Stalemate

    # Add current position to history
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
    Returns (best_move, score).
    """
    if history is None:
        history = set()

    best_move = None
    alpha = -INFINITY
    beta = INFINITY
    
    moves = generate_legal_moves(pos)
    
    if not moves:
        return None, 0  # No legal moves
    
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