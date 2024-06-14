# src/Registry/element.py
from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.bls import combine, scale
from src.Registry.element import Element
from src.sha3_256 import fiat_shamir_heuristic

if TYPE_CHECKING:
    from src.Registry.registry import Registry


@dataclass
class Schnorr:
    z: str
    r: Element
    registry: 'Registry'

    def __str__(self):
        return f"Schnorr(z={self.z}, r={self.r}, registry={self.registry})"

    def prove(self) -> bool:
        g_z = scale(self.registry.g.value, int(self.z, 16))
        c_hex = fiat_shamir_heuristic(self.registry.g.value, self.r.value, self.registry.u.value)
        u_c = scale(self.registry.u.value, int(c_hex, 16))
        rhs = combine(self.r.value, u_c)
        return g_z == rhs
