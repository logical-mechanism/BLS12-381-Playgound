from dataclasses import dataclass, field

from src.bls import point, rng, scale
from src.Registry.element import Element
from src.Registry.fiat_shamir import FiatShamir
from src.Registry.schnorr import Schnorr
from src.sha3_256 import fiat_shamir_heuristic, generate


def hexify(n: int) -> str:
    hex_n = hex(n)[2:]  # Remove the '0x' prefix
    if len(hex_n) % 2 != 0:
        hex_n = '0' + hex_n  # Prepend '0' if length is odd
    return hex_n


@dataclass
class Registry:
    x: int | None = None
    g: Element = field(init=False)
    u: Element = field(init=False)

    def __post_init__(self):
        if self.x is None:
            self.x = rng()
        self.g = Element(point(1))
        self.u = Element(point(self.x))

    def __str__(self):
        return f"Registry(g={self.g}, u={self.u})"

    def rerandomize(self, scalar: int | None) -> None:
        if scalar is None:
            scalar = rng()
        self.g = Element(scale(self.g.value, scalar))
        self.u = Element(scale(self.u.value, scalar))

    def rng(self) -> int:
        return rng()

    def schnorr_signature(self) -> Schnorr:
        r = rng()
        g_r = scale(self.g.value, r)
        c_hex = fiat_shamir_heuristic(self.g.value, g_r, self.u.value)
        c = int(c_hex, 16)
        z = r + c * self.x
        return Schnorr(hexify(z), Element(g_r), self)

    def fiat_shamir_signature(self, message: str):
        m = generate(message)
        r = rng()
        g_r = scale(self.g.value, r)
        eb = generate(m + g_r)
        e = int(eb, 16)
        z = r + self.x * e
        return FiatShamir(message, hexify(z), Element(g_r), self)
