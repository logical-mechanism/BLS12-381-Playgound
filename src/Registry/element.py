# src/Registry/element.py
from dataclasses import dataclass

from src.bls import combine, compress, scale, uncompress
from src.sha3_256 import generate


@dataclass
class Element:
    value: str

    def compressed(self) -> str:
        return compress(self.value)

    def uncompressed(self) -> tuple:
        return uncompress(self.value)

    def hash(self) -> str:
        return generate(self.value)

    def __str__(self):
        return self.value

    def __add__(self, other):
        if not isinstance(other, Element):
            return NotImplemented
        return Element(combine(self.value, other.value))

    def __mul__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return Element(scale(self.value, other))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __eq__(self, other):
        if not isinstance(other, Element):
            return NotImplemented
        # Equality logic based on value
        return self.value == other.value
