from dataclasses import dataclass, field

from src.bls12_381 import field_order, point
from src.Registry.element import Element


@dataclass
class Range:
    d: int
    a: int | None = None
    b: int | None = None
    A: Element = field(init=False)
    B: Element = field(init=False)
    D: Element = field(init=False)
    Y: Element = field(init=False)
    W: Element = field(init=False)

    def __post_init__(self):
        # set up A
        if self.a is None:
            self.a = field_order - 1
        self.A = Element(point(self.a))

        # set up B
        if self.b is None:
            self.b = 1
        self.B = Element(point(self.b))

        # Set up D
        self.D = Element(point(self.d))

        # Set up Y
        y = self.a - self.d
        self.Y = Element(point(y))

        # Set up W
        w = self.d - self.b
        self.W = Element(point(w))

    def __str__(self):
        return f"Range(A={self.A.value}, B={self.B.value}, D={self.D.value}, Y={self.Y.value}, W={self.W.value})"

    def prove(self) -> bool:
        # Check the validity of the range proof by verifying the provided equations
        return self.A == self.B + self.Y + self.W and self.A + self.B + self.W == 2 * self.D + self.Y
