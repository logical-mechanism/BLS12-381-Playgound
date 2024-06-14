# src/Registry/element.py
from dataclasses import dataclass
from typing import TYPE_CHECKING

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
        return f"Schnorr(z={self.z}, r={self.r.value}, registry={self.registry})"

    def prove(self) -> bool:
        z = int(self.z, 16)
        g_z = self.registry.g * z
        c_hex = fiat_shamir_heuristic(self.registry.g.value, self.r.value, self.registry.u.value)
        c = int(c_hex, 16)
        u_c = self.registry.u * c
        rhs = self.r + u_c
        return g_z == rhs
