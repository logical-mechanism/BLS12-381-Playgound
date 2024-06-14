import copy

from src.bls import combine, rng, scale
from src.Registry.registry import Registry
from src.sha3_256 import generate


def proveDHTuple(scalar: int, left: Registry, right: Registry) -> bool:
    r = rng()
    left_copy = copy.deepcopy(left)
    left_copy.rerandomize(r)
    cb = generate(left_copy.g.value + left_copy.u.value)
    c = int(cb, 16)
    z = r + c * scalar

    a_z = scale(left.g.value, z)
    a0_c = scale(right.g.value, c)
    t0_a0_c = combine(left_copy.g.value, a0_c)

    b_z = scale(left.u.value, z)
    b0_c = scale(right.u.value, c)
    t1_b0_c = combine(left_copy.u.value, b0_c)

    return a_z == t0_a0_c and b_z == t1_b0_c and scalar != 0 and right.g.value != right.u.value
