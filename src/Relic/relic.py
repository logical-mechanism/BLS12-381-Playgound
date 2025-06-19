# This class is special built just for cswilm-pre
#
from __future__ import annotations
from dataclasses import dataclass, field
from src.Registry.element import Element
from src.Relic.cramer_shoup import CramerShoup
from src.bls12_381 import g1_point, rng
from src.reversible_mapping import map_to_point, point_to_map
from src.sha3_256 import hash_to_int


@dataclass
class Relic:
    # Secret keys
    x1: int | None = None
    x2: int | None = None
    y1: int | None = None
    y2: int | None = None
    z: int | None = None

    # Fix field elements
    g: Element = field(default_factory=lambda: Element(g1_point(1)))
    u: Element = field(default_factory=lambda: Element(g1_point(2)))

    # public elements
    c: Element = field(init=False)
    d: Element = field(init=False)
    h: Element = field(init=False)

    def __post_init__(self):
        if self.x1 is None:
            self.x1 = rng()

        if self.x2 is None:
            self.x2 = rng()

        if self.y1 is None:
            self.y1 = rng()

        if self.y2 is None:
            self.y2 = rng()

        if self.z is None:
            self.z = rng()

        self.c = self.x1 * self.g + self.x2 * self.u
        self.d = self.y1 * self.g + self.y2 * self.u
        self.h = self.z * self.g

    def __str__(self):
        return f"Relic(c={self.c}, d={self.d}, h={self.h})"

    def encrypt(self, message: str) -> CramerShoup:
        point, offset = map_to_point(message)
        M = Element(point)

        k = rng()
        u1 = k * self.g
        u2 = k * self.u
        e = k * self.h + M
        alpha = hash_to_int(u1.value + u2.value + e.value)
        v = k * self.c + (k * alpha) * self.d

        return CramerShoup(u1, u2, e, v, offset)

    def prove(self, cyphertext: CramerShoup) -> bool:
        if self.x1 is None or self.x2 is None or self.y1 is None or self.y2 is None:
            return False
        alpha = hash_to_int(
            cyphertext.u1.value + cyphertext.u2.value + cyphertext.e.value
        )
        return (
            self.x1 * cyphertext.u1
            + self.x2 * cyphertext.u2
            + (self.y1 * alpha) * cyphertext.u1
            + (self.y2 * alpha) * cyphertext.u2
            == cyphertext.v
        )

    def extract(self, cyphertext: CramerShoup) -> str:
        h_k = self.z * cyphertext.u1
        s = ~h_k
        m = cyphertext.e + s
        return point_to_map(m.value, cyphertext.o)
