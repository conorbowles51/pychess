import sys
from .fen import parse_fen
from .position import Position
from .search import search
from .makeunmake import make_move
from .move import Move
from .bitboard import uci_to_sq
from .zobrist import hash_position

def parse_move(uci_str: str) -> Move:
    """Convert UCI string like 'e2e4' or 'e7e8q' to a Move object."""
    from_sq = uci_to_sq(uci_str[0:2])
    to_sq = uci_to_sq(uci_str[2:4])
    promo = uci_str[4] if len(uci_str) == 5 else None
    return Move(from_sq, to_sq, promo)


def parse_position(tokens: list[str]) -> Position:
    """Parse 'position startpos moves e2e4 e7e5' or 'position fen <fen> moves ...'"""
    idx = 1
    history = set()
    
    if tokens[idx] == "startpos":
        pos = parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        idx = 2
    elif tokens[idx] == "fen":
        # FEN is 6 space-separated parts
        fen_parts = tokens[2:8]
        fen = " ".join(fen_parts)
        pos = parse_fen(fen)
        idx = 8

    # Add starting position to history
    history.add(hash_position(pos))
    
    # Apply moves if present
    if idx < len(tokens) and tokens[idx] == "moves":
        idx += 1
        while idx < len(tokens):
            move = parse_move(tokens[idx])
            pos = make_move(pos, move)
            history.add(hash_position(pos))  # Track each position
            idx += 1
    
    return pos, history

def parse_go(tokens: list[str]) -> int:
    """Parse 'go depth 5' and return the depth. Default to 4 if not specified."""
    depth = 5  # Default depth
    
    for i, token in enumerate(tokens):
        if token == "depth" and i + 1 < len(tokens):
            depth = int(tokens[i + 1])
            break
    
    return depth

def uci_loop():
    """Main UCI protocol loop."""
    pos = None
    history = set()
    
    while True:
        try:
            line = input().strip()
        except EOFError:
            break
        
        if not line:
            continue
        
        tokens = line.split()
        cmd = tokens[0]
        
        if cmd == "uci":
            print("id name CB-PyChess")
            print("id author ConorBowles")
            print("uciok")
        
        elif cmd == "isready":
            print("readyok")
        
        elif cmd == "ucinewgame":
            pos = None
            history = set()  # Clear history for new game
        
        elif cmd == "position":
            pos, history = parse_position(tokens)
        
        elif cmd == "go":
            depth = parse_go(tokens)
            if pos:
                best_move, score = search(pos, depth, history)
                if best_move:
                    print(f"bestmove {best_move.to_uci()}")
                else:
                    print("bestmove 0000")
        
        elif cmd == "quit":
            break
        
        # Flush output so GUI receives it immediately
        sys.stdout.flush()