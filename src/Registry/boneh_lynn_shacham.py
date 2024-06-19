# src/Registry/element.py
from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.Registry.element import Element
from src.sha3_256 import generate

if TYPE_CHECKING:
    from src.Registry.registry import Registry


@dataclass
class BonehLynnShacham:
    m: str
    z: str
    r: Element
    registry: 'Registry'

    def __str__(self):
        return f"BonehLynnShacham (m={self.m}, z={self.z}, r={self.r.value}, registry={self.registry})"

    def prove(self) -> bool:
        m = generate(self.m)
        eb = generate(m + self.r.value)
        e = int(eb, 16)
        z = int(self.z, 16)
        g_z = self.registry.g * z
        u_e = self.registry.u * e
        rhs = self.r + u_e
        return g_z == rhs
