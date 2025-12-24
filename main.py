from engine.fen import parse_fen
from engine.position import pretty

START = "kkbqkbnr/pppppppp/8/6pP/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
pos = parse_fen(START)
print(pretty(pos))
