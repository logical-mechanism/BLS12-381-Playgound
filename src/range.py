from src.bls import field_order, point
from src.Registry.element import Element


def prove(range_proof: dict) -> bool:
    A = range_proof["a"]
    B = range_proof["b"]

    D = range_proof["d"]
    Y = range_proof["y"]
    W = range_proof["w"]

    return A == B + Y + W and A + B + W == 2 * D + Y


def generate(d: int, a: int = field_order - 1, b: int = 1) -> dict:
    y = a - d
    w = d - b

    return {
        'a': Element(point(a)),
        'b': Element(point(b)),
        'd': Element(point(d)),
        'y': Element(point(y)),
        'w': Element(point(w)),
    }
