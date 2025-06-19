from dataclasses import dataclass

from src.Registry.element import Element


@dataclass
class CramerShoup:
    u1: Element
    u2: Element
    e: Element
    v: Element
    o: int

    def __str__(self):
        return f"Cramer-Shoup(u1={self.u1.value}, u2={self.u2.value}, e={self.e.value}, v={self.v.value})"
        