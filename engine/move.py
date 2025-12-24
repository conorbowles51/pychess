from dataclasses import dataclass
from .bitboard import sq_to_uci

@dataclass(frozen=True, slots=True)
class Move:
    from_sq: int
    to_sq: int
    promo: str | None = None

    def to_uci(self) -> str:
        if self.promo:
            return f"{sq_to_uci(self.from_sq)}{sq_to_uci(self.to_sq)}{self.promo}"
        return f"{sq_to_uci(self.from_sq)}{sq_to_uci(self.to_sq)}"