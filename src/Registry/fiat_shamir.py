# src/Registry/element.py
from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.bls import combine, scale
from src.Registry.element import Element
from src.sha3_256 import generate

if TYPE_CHECKING:
    from src.Registry.registry import Registry


@dataclass
class FiatShamir:
    m: str
    z: str
    r: Element
    registry: 'Registry'

    def __str__(self):
        return f"FiatShamir(m={self.m}, z={self.z}, r={self.r}, registry={self.registry})"

    def prove(self) -> bool:
        m = generate(self.m)
        eb = generate(m + self.r.value)
        g_z = scale(self.registry.g.value, int(self.z, 16))
        u_e = scale(self.registry.u.value, int(eb, 16))
        rhs = combine(self.r.value, u_e)
        return g_z == rhs
