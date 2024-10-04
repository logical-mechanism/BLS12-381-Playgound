import pytest
from py_ecc.optimized_bls12_381 import field_modulus as p

from src.reversible_mapping import (find_valid_point, map_to_point,
                                    point_to_map, short_weierstrass_form,
                                    string_to_int, verify_point_on_curve)


def test_string_to_int():
    d = "Hello World"
    assert string_to_int(d) == 87521618088882533792115812


def test_short_weierstrass_form():
    x = 123
    result = short_weierstrass_form(x)
    assert 1860871 == result


def test_find_valid_point1():
    s = "A Secret String"
    d = string_to_int(s)
    x, y, o = find_valid_point(d)
    assert pow(y, 2, p) == (pow(x + o, 3, p) + 4) % p


def test_find_valid_point2():
    s = "random strings of length 32 here"
    d = string_to_int(s)
    x, y, o = find_valid_point(d)
    assert pow(y, 2) % p == (pow(x + o, 3) + 4) % p


def test_is_point_on_curve():
    s = "A Secret String"
    d = string_to_int(s)
    x, y, o = find_valid_point(d)
    point = (x + o, y)
    assert verify_point_on_curve(point)


def test_compress_point1():
    s = "ffffffffffffffffffffffffffffffff"
    point, offset = map_to_point(s)
    assert point_to_map(point, offset) == s


def test_compress_point2():
    s = "random strings of length 32 here"
    point, offset = map_to_point(s)
    assert point_to_map(point, offset) == s


if __name__ == "__main__":
    pytest.main()
