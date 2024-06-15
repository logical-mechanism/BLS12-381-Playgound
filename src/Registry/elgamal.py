# src/Registry/element.py
from dataclasses import dataclass

from src.Registry.element import Element
from src.sha3_256 import generate


@dataclass
class ElGamal:
    c1: Element
    c2: Element
    h: str

    def __str__(self):
        return f"ElGamal(c1={self.c1.value}, c2={self.c2.value}, h={self.h})"

    def prove(self, cipher_key: Element) -> bool:
        s = ~cipher_key
        m = self.c2 + s
        return generate(m.value) == self.h
