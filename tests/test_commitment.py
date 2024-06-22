import pytest

from src.bls12_381 import g1_identity, g1_point, scale
from src.commitment import Commitment


def test_null_commitment():
    c = Commitment(r=0, v=0)
    assert c.c.value == g1_identity


def test_zero_value():
    c = Commitment(r=44203, v=0)
    assert c.c.value == g1_point(44203)


def test_zero_random():
    c = Commitment(r=0, v=44203)
    assert c.c.value == scale(g1_point(2), 44203)


def test_combine_commitments():
    v0 = 123456789
    v1 = 987654321
    c0 = Commitment(v=v0)
    c1 = Commitment(v=v1)
    ct = c0 + c1
    assert ct.v == v0 + v1
    assert ct.r == c0.r + c1.r


if __name__ == "__main__":
    pytest.main()
