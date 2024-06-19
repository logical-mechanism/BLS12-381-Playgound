# src/Registry/element.py
from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.bls12_381 import pair
from src.Registry.element import Element

if TYPE_CHECKING:
    from src.Registry.registry import Registry


@dataclass
class BonehLynnShacham:
    s: Element
    m: Element
    registry: 'Registry'

    def __str__(self):
        return f"BonehLynnShacham (s={self.s}, registry={self.registry})"

    def __add__(self, other: 'BonehLynnShacham') -> 'BonehLynnShacham':
        if self.registry != other.registry:
            raise ValueError("Cannot aggregate signatures from different registries")
        aggregated_s = self.s + other.s
        aggregated_m = self.m + other.m
        return BonehLynnShacham(aggregated_s, aggregated_m, self.registry)

    def prove(self) -> bool:
        return pair(self.s.value, self.registry.g.value) == pair(self.m.value, self.registry.u.value)
