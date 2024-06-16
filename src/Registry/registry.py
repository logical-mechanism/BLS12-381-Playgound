from dataclasses import dataclass, field

from src.bls12_381 import g1_point, rng
from src.Registry.element import Element
from src.Registry.elgamal import ElGamal
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
        self.g = Element(g1_point(1))
        self.u = Element(g1_point(self.x))

    def __str__(self):
        return f"Registry(g={self.g}, u={self.u})"

    def rerandomize(self, scalar: int | None) -> None:
        if scalar is None:
            scalar = rng()
        self.g = self.g * scalar
        self.u = self.u * scalar

    def rng(self) -> int:
        return rng()

    def schnorr_signature(self) -> Schnorr:
        r = self.rng()
        g_r = self.g * r
        c_hex = fiat_shamir_heuristic(self.g.value, g_r.value, self.u.value)
        c = int(c_hex, 16)
        z = r + c * self.x
        return Schnorr(hexify(z), g_r, self)

    def fiat_shamir_signature(self, message: str):
        m = generate(message)
        r = self.rng()
        g_r = self.g * r
        eb = generate(m + g_r.value)
        e = int(eb, 16)
        z = r + self.x * e
        return FiatShamir(message, hexify(z), g_r, self)

    def elgamal_encryption(self, message: str):
        msg_hash = generate(message)
        m = int(msg_hash, 16)
        M = Element(g1_point(m))
        r = self.rng()
        s = self.u * r
        c1 = self.g * r
        c2 = M + s
        return ElGamal(c1, c2, generate(M.value))
