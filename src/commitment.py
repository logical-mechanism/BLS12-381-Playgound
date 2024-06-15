from dataclasses import dataclass, field

from src.bls import point, rng
from src.Registry.element import Element


@dataclass
class Commitment:
    v: int
    r: int | None = None
    c: Element = field(init=False)

    def __post_init__(self):
        # this are fixed inside of a commitment
        g = Element(point(1))
        h = Element(point(2))
        # unique to this commitment
        if self.r is None:
            self.r = rng()
        self.c = self.r * g + self.v * h

    def __str__(self):
        return f"Commitment(c={self.c.value}, r={self.r}, v={self.v})"

    def __add__(self, other):
        if not isinstance(other, Commitment):
            return NotImplemented
        # Combine the c elements
        combined_c = self.c + other.c
        # Add the r values
        combined_r = self.r + other.r
        # Add the v values
        combined_v = self.v + other.v
        # Create a new Commitment instance with combined values
        new_commitment = Commitment(combined_v)
        new_commitment.r = combined_r
        new_commitment.c = combined_c
        return new_commitment

    def __eq__(self, other):
        if not isinstance(other, Commitment):
            return NotImplemented
        return self.c == other.c and self.r == other.r and self.v == other.v
