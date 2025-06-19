from dataclasses import dataclass

from src.Registry.element import Element
from src.sha3_256 import generate, hash_to_int
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
        # simple hack to make it work with the registry class
        x1 = secret_key
        x2 = hash_to_int(str(x1))
        y1 = hash_to_int(str(x2))
        y2 = hash_to_int(str(y1))

        alpha = hash_to_int(self.u1.value + self.u2.value + self.e.value)

        return x1 * self.u1 + x2 * self.u2 + (y1 * alpha) * self.u1 + (y2 * alpha) * self.u2 == self.v

    def extract(self, secret_key: int) -> str:
        # simple hack to make it work with the registry class
        x1 = secret_key
        x2 = hash_to_int(str(x1))
        y1 = hash_to_int(str(x2))
        y2 = hash_to_int(str(y1))
        z = hash_to_int(str(y2))

        h_k = z * self.u1
        s = ~h_k
        m = self.e + s
        return point_to_map(m.value, self.o)
        