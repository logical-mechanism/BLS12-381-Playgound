from dataclasses import dataclass, field

from src.bls12_381 import g1_point, rng
from src.Registry.element import Element
from src.sha3_256 import generate


@dataclass
class Commitment:
    v: int
    r: int | None = None

    c: Element = field(init=False)

    def __post_init__(self):
        # this are fixed inside of a commitment
        g = Element(g1_point(1))
        h = Element(g1_point(2))
        # unique to this commitment
        if self.r is None:
            self.r = rng()
        self.c = self.r * g + self.v * h

    def hash(self) -> str:
        return generate(self.c.value)

    def __str__(self):
        return f"Commitment(c={self.c.value}, r={self.r}, v={self.v})"

    def __add__(self, other):
        if not isinstance(other, Commitment):
            return NotImplemented
        # Add the r values
        combined_r = self.r + other.r
        # Add the v values
        combined_v = self.v + other.v
        # Create a new Commitment instance with combined values
        return Commitment(combined_v, combined_r)

    def __eq__(self, other):
        if not isinstance(other, Commitment):
            return NotImplemented
        return self.c == other.c and self.r == other.r and self.v == other.v
