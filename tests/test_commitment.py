import pytest

from src.bls12_381 import field_order, g1_identity, g1_point, scale
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
    assert ct.r == (c0.r + c1.r) % field_order


def test_identity_commitment():
    v = 123456789
    r = 987654321
    c = Commitment(v=v, r=r)
    identity_commitment = Commitment(v=0, r=0)
    combined_commitment = c + identity_commitment
    assert combined_commitment.v == c.v
    assert combined_commitment.r == c.r
    assert combined_commitment.c.value == c.c.value


def test_commitment_addition_commutativity():
    v0 = 123456789
    v1 = 987654321
    c0 = Commitment(v=v0)
    c1 = Commitment(v=v1)
    assert (c0 + c1).c.value == (c1 + c0).c.value


def test_commitment_addition_associativity():
    v0 = 111111111
    v1 = 222222222
    v2 = 333333333
    c0 = Commitment(v=v0)
    c1 = Commitment(v=v1)
    c2 = Commitment(v=v2)
    assert ((c0 + c1) + c2).c.value == (c0 + (c1 + c2)).c.value


def test_commitment_homomorphism():
    v = 123456789
    c = Commitment(v=v)
    double_commitment = c + c
    scaled_commitment = Commitment(v=2 * v, r=2 * c.r)
    assert double_commitment.c.value == scaled_commitment.c.value


def test_different_randomness():
    v = 123456789
    c0 = Commitment(v=v, r=44203)
    c1 = Commitment(v=v, r=12345)
    assert c0.c.value != c1.c.value


def test_commitment_equality():
    v = 123456789
    r = 44203
    c0 = Commitment(v=v, r=r)
    c1 = Commitment(v=v, r=r)
    assert c0 == c1


def test_subtract_from_commit():
    w = Commitment(2)
    r = Commitment(0, w.r)
    answer = Commitment(2, 0)
    assert w - r == answer


def test_knowledge_of_r():
    v = 123456789
    r = 44203
    c0 = Commitment(v=v, r=r)
    assert c0.prove_knowledge_of_r(v)


if __name__ == "__main__":
    pytest.main()
