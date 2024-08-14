from src.bls12_381 import g1_identity, g1_point, invert
from src.Registry.element import Element


def test_adding_two_elements():
    a = Element(g1_point(42))
    b = Element(g1_point(58))
    c = Element(g1_point(100))
    assert a + b == c


def test_subbing_two_elements():
    a = Element(g1_point(42))
    b = Element(invert(g1_point(58)))
    c = Element(g1_point(100))
    assert c + b == a


def test_adding_identity():
    a = Element(g1_identity)
    b = Element(g1_identity)
    c = Element(g1_identity)
    assert a + b == c
