from dataclasses import dataclass

from src.Registry.element import Element
from src.reversible_mapping import point_to_map
from src.sha3_256 import generate


@dataclass
class ReverseMapping:
    c1: Element
    c2: Element
    h: str
    o: int

    def __str__(self):
        return f"ReverseMapping(c1={self.c1.value}, c2={self.c2.value}, h={self.h}, o={self.o})"

    def prove(self, cipher_key: Element) -> bool:
        s = ~cipher_key
        m = self.c2 + s
        message = point_to_map(m.value, self.o)
        return generate(message) == self.h

    def extract(self, cipher_key: Element) -> str:
        s = ~cipher_key
        m = self.c2 + s
        return point_to_map(m.value, self.o)
