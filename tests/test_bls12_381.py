import pytest

from src.bls12_381 import (combine, compress, g1_identity, g1_point,
                           g2_identity, g2_point, gt_identity, invert, pair,
                           scale, uncompress)


def test_g1_identity():
    g0 = g1_point(0)
    assert g0 == g1_identity


def test_g2_identity():
    g0 = g2_point(0)
    assert g0 == g2_identity


def test_g1_compress_is_uncompressed():
    scalar = 123456789  # Example scalar value
    compressed_g1_point = g1_point(scalar)
    uncompressed_g1_point = uncompress(compressed_g1_point)
    recompressed_g1_point = compress(uncompressed_g1_point)
    assert recompressed_g1_point == compressed_g1_point


def test_g2_compress_is_uncompressed():
    scalar = 123456789  # Example scalar value
    compressed_g2_point = g2_point(scalar)
    uncompressed_g2_point = uncompress(compressed_g2_point)
    recompressed_g2_point = compress(uncompressed_g2_point)
    assert recompressed_g2_point == compressed_g2_point


def test_g1_invert_of_an_invert_is_equal():
    g1 = g1_point(1)
    gi = invert(g1)
    g = invert(gi)
    assert uncompress(g1) == uncompress(g)


def test_g2_invert_of_an_invert_is_equal():
    g2 = g2_point(1)
    gi = invert(g2)
    g = invert(gi)
    assert uncompress(g2) == uncompress(g)


def test_g1_one_plus_one_equals_two():
    g1 = g1_point(1)
    added_g1 = combine(g1, g1)
    assert added_g1 == g1_point(2)


def test_g2_one_plus_one_equals_two():
    g2 = g2_point(1)
    added_g2 = combine(g2, g2)
    assert added_g2 == g2_point(2)


def test_bilinear_pairing():
    u1g1 = g1_point(1)
    u2g1 = g1_point(2)
    v1g2 = g2_point(1)
    v2g2 = g2_point(2)

    # e(U1+U2,V1)=e(U1,V1) x e(U2,V1)
    pr = pair(v1g2, combine(u1g1, u2g1))
    pl = pair(v1g2, u1g1) * pair(v1g2, u2g1)
    assert pr == pl

    # e(U1,V1+V2)=e(U1,V1) x e(U1,V2)
    pl = pair(combine(v1g2, v2g2), u1g1)
    pr = pair(v1g2, u1g1) * pair(v2g2, u1g1)
    assert pr == pl


def test_computational_bilinearity():
    u1g1 = g1_point(1)
    v1g2 = g2_point(1)

    a = 20
    b = 10
    au = scale(u1g1, a)
    bv = scale(v1g2, b)

    # e(aU,bV)=e(U,V)^(a*b)
    pl = pair(bv, au)
    pr = pair(v1g2, u1g1) ** (a * b)
    pr2 = pair(v1g2, scale(u1g1, a * b))
    pr3 = pair(scale(v1g2, a * b), u1g1)
    assert pr == pl
    assert pl == pr2
    assert pr2 == pr3


def test_exponent_identity():
    u1g1 = g1_point(1)
    v1g2 = g2_point(1)

    # e(G,H)^k=1, k = 0
    assert pair(v1g2, u1g1) ** 0 == gt_identity

    # e(Q,P)^(x^2 - x - 42)=1, x^2 - x - 42 = 0
    assert pair(scale(v1g2, 7), scale(u1g1, 7)) * pair(invert(v1g2), scale(u1g1, 7)) * pair(invert(v1g2), scale(u1g1, 42)) == gt_identity


if __name__ == "__main__":
    pytest.main()
