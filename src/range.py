from dataclasses import dataclass, field

from src.bls12_381 import (field_order, g1_point, g2_point, gt_identity,
                           invert, pair)
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
    Q: Element = Element(g2_point(1))
    QI: Element = invert(Q.value)

    def __post_init__(self):
        # set up A
        if self.a is None:
            self.a = field_order - 1
        self.A = Element(g1_point(self.a))

        # set up B
        if self.b is None:
            self.b = 1
        self.B = Element(g1_point(self.b))

        # Set up D
        self.D = Element(g1_point(self.d))

        # Set up Y
        y = self.a - self.d
        self.Y = Element(g1_point(y))

        # Set up W
        w = self.d - self.b
        self.W = Element(g1_point(w))

    def __str__(self):
        return f"Range(A={self.A.value}, B={self.B.value}, D={self.D.value}, Y={self.Y.value}, W={self.W.value})"

    def prove(self) -> bool:
        return pair(self.Q.value, (self.Y + 2 * self.D).value) * pair(self.QI, (self.A + self.B + self.W).value) == gt_identity
