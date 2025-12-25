from .position import Position
from .movegen import generate_legal_moves, is_checkmate, is_in_check, is_stalemate
from .makeunmake import make_move
from .evaluation import evaluate
from .move import Move

INFINITY = 999_999
CHECKMATE_SCORE = 100_000

def negamax(pos: Position, depth: int, alpha: int, beta: int) -> int:
    if depth == 0:
        score = evaluate(pos)
        return score if pos.side_to_move == "w" else -score
    
    moves = generate_legal_moves(pos)

    if not moves:
        if is_in_check(pos):
            return -CHECKMATE_SCORE # Checkmate
        return 0 # Stalemate

    for move in moves:
        new_pos = make_move(pos, move)
        score = -negamax(new_pos, depth - 1, -beta, -alpha)

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha


def search(pos: Position, depth: int) -> tuple[Move | None, int]:
    """
    Search for the best move.
    Returns (best_move, score).
    """
    best_move = None
    alpha = -INFINITY
    beta = INFINITY
    
    moves = generate_legal_moves(pos)
    
    if not moves:
        return None, 0  # No legal moves
    
    for move in moves:
        new_pos = make_move(pos, move)
        score = -negamax(new_pos, depth - 1, -beta, -alpha)
        
        if score > alpha:
            alpha = score
            best_move = move
    
    return best_move, alpha