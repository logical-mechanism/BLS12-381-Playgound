# src/Registry/element.py
from dataclasses import dataclass

from src.bls import compress, uncompress
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
