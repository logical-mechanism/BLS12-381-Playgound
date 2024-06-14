from src.bls import combine, field_order, point, scale


def prove(range_proof: dict) -> bool:
    A = range_proof["a"]
    B = range_proof["b"]

    D = range_proof["d"]
    Y = range_proof["y"]
    W = range_proof["w"]

    return A == combine(combine(B, Y), W) and combine(combine(A, B), W) == combine(scale(D, 2), Y)


def generate(d: int, a: int = field_order - 1, b: int = 1) -> dict:
    y = a - d
    w = d - b

    return {
        'a': point(a),
        'b': point(b),
        'd': point(d),
        'y': point(y),
        'w': point(w),
    }
