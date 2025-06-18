from dataclasses import dataclass

from src.Registry.element import Element
from src.sha3_256 import generate
from src.reversible_mapping import point_to_map


@dataclass
class CramerShoup:
    u1: Element
    u2: Element
    e: Element
    v: Element
    o: int

    def __str__(self):
        return f"Cramer-Shoup(u1={self.u1.value}, u2={self.u2.value}, e={self.e.value}, v={self.v.value})"

    def prove(self, secret_key: int) -> bool:
        x1 = secret_key
        x2 = int(generate(str(x1)), 16)
        y1 = int(generate(str(x2)), 16)
        y2 = int(generate(str(y1)), 16)

        alpha = int(generate(self.u1.value + self.u2.value + self.e.value), 16)

        return x1 * self.u1 + x2 * self.u2 + (y1 * alpha) * self.u1 + (y2 * alpha) * self.u2 == self.v

    def extract(self, secret_key: int) -> str:
        x1 = secret_key
        x2 = int(generate(str(x1)), 16)
        y1 = int(generate(str(x2)), 16)
        y2 = int(generate(str(y1)), 16)
        z = int(generate(str(y2)), 16)

        h_k = z * self.u1
        s = ~h_k
        m = self.e + s
        return point_to_map(m.value, self.o)
        