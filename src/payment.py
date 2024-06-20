from dataclasses import dataclass, field

from py_ecc.fields import optimized_bls12_381_FQ12 as FQ12

from src.bls12_381 import g1_identity, g1_point, g2_point, invert, pair
from src.Registry.boneh_lynn_shacham import BonehLynnShacham
from src.Registry.element import Element
from src.Registry.registry import Registry


@dataclass
class Payment:
    s: BonehLynnShacham
    initial: tuple[int, int, int]
    final: tuple[int, int, int]
    receiver: Registry
    f: int
    b: int
    A: Element = field(init=False)
    B: Element = field(init=False)
    P: Element = Element(g1_point(1))
    Q: Element = Element(g2_point(1))
    QI: Element = field(init=False)

    def __post_init__(self):
        self.QI = invert(self.Q.value)
        self.A = Element(g1_identity)
        for i in self.initial:
            p = Element(g1_point(i))
            self.A = self.A + p

        self.B = Element(g1_identity)
        for f in self.final:
            p = Element(g1_point(f))
            self.B = self.B + p

    def prove(self) -> bool:
        value_conservation = pair(self.Q.value, self.A.value) * pair(self.QI, self.B.value) == FQ12.one()
        spend_validation = self.s.prove()
        return all([value_conservation, spend_validation])
