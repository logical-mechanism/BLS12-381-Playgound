import copy

from src.Registry.registry import Registry
from src.sha3_256 import generate


def proveDHTuple(scalar: int, left: Registry, right: Registry) -> bool:
    r = left.rng()
    left_copy = copy.deepcopy(left)
    left_copy.rerandomize(r)
    cb = generate(left_copy.g.value + left_copy.u.value)
    c = int(cb, 16)
    z = r + c * scalar

    a_z = left.g * z
    a0_c = right.g * c
    t0_a0_c = left_copy.g + a0_c

    b_z = left.u * z
    b0_c = right.u * c
    t1_b0_c = left_copy.u + b0_c

    return a_z == t0_a0_c and b_z == t1_b0_c and scalar != 0 and right.g.value != right.u.value
