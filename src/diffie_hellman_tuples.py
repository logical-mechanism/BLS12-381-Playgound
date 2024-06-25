import copy

from src.Registry.registry import Registry
from src.sha3_256 import generate


def proveDHTuple(scalar: int, left: Registry, right: Registry) -> bool:
    """
    Proves a discrete logarithm tuple (DH tuple) using a provided scalar.

    Parameters:
    scalar (int): The scalar value used in the proof.
    left (Registry): The left-hand side registry object.
    right (Registry): The right-hand side registry object.

    Returns:
    bool: True if the proof is valid, False otherwise.
    """
    # Generate a random value r
    r = left.rng()

    # Create a deep copy of the left registry object and rerandomize it with r
    left_copy = copy.deepcopy(left)
    left_copy.rerandomize(r)
    right_copy = copy.deepcopy(right)
    right_copy.rerandomize(r)

    # Generate a challenge c based on the concatenation of the values in the left_copy registry
    cb = generate(left_copy.g.value + right_copy.g.value)
    c = int(cb, 16)

    # Calculate z as r + c * scalar
    z = r + c * scalar

    # Compute a_z as g^z in the left registry
    a_z = left.g * z

    # Compute t0_a0_c as the sum of g in left_copy and g^c in the right registry
    a0_c = right.g * c
    t0_a0_c = left_copy.g + a0_c

    # Compute b_z as u^z in the left registry
    b_z = left.u * z

    # Compute t1_b0_c as the sum of u in left_copy and u^c in the right registry
    b0_c = right.u * c
    t1_b0_c = left_copy.u + b0_c

    # Check if the computed values match and if scalar is non-zero and g and u are distinct
    return a_z == t0_a0_c and b_z == t1_b0_c and scalar != 0 and right.g.value != right.u.value
