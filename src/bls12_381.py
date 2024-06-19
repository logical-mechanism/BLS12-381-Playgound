import secrets

from py_ecc.bls.g2_primitives import (G1_to_pubkey, G2_to_signature,
                                      pubkey_to_G1, signature_to_G2)
from py_ecc.bls.hash_to_curve import hash_to_G2
from py_ecc.fields import optimized_bls12_381_FQ as FQ
from py_ecc.fields import optimized_bls12_381_FQ2 as FQ2
from py_ecc.fields import optimized_bls12_381_FQ12 as FQ12
from py_ecc.optimized_bls12_381 import (G1, G2, Z1, Z2, add, curve_order,
                                        multiply, neg, pairing)

from src.sha3_256 import hash_function

field_order = curve_order


def rng() -> int:
    """
    Generates a random hex string of the specified length using the secrets module.

    Returns:
        int: A random number below the field order.
    """
    # Generate a random byte string of the specified length
    random_bits = secrets.randbits(255)
    if random_bits < field_order:
        return random_bits
    else:
        return rng()


def g2_point(scalar: int) -> str:
    """
    Generates a BLS12-381 point from the G2 generator using scalar multiplication
    and returns it in compressed format.

    Args:
        scalar (int): The scalar value for multiplication.

    Returns:
        bytes: The resulting BLS12-381 G2 point in compressed format.
    """
    return G2_to_signature(multiply(G2, scalar)).hex()


def g1_point(scalar: int) -> str:
    """
    Generates a BLS12-381 point from the G1 generator using scalar multiplication
    and returns it in compressed format.

    Args:
        scalar (int): The scalar value for multiplication.

    Returns:
        bytes: The resulting BLS12-381 G1 point in compressed format.
    """
    return G1_to_pubkey(multiply(G1, scalar)).hex()


def uncompress(element: str) -> tuple:
    """
    Uncompresses a hexadecimal string to a BLS12-381 point.

    Args:
        element (str): The compressed point as a hexadecimal string.

    Returns:
        tuple: The uncompressed point.
    """
    if len(element) == 96:
        return pubkey_to_G1(bytes.fromhex(element))
    else:
        return signature_to_G2(bytes.fromhex(element))


def compress(element: tuple) -> str:
    """
    Compresses a BLS12-381 point to a hexadecimal string.

    Args:
        element (tuple): The point to be compressed.

    Returns:
        str: The compressed point as a hexadecimal string.
    """
    if isinstance(element[2], FQ):
        return G1_to_pubkey(element).hex()
    if isinstance(element[2], FQ2):
        return G2_to_signature(element).hex()


def scale(element: str, scalar: int) -> str:
    """
    Scales a BLS12-381 point by a given scalar using scalar multiplication.

    Args:
        element (str): The compressed point to be scaled.
        scalar (int): The scalar value for multiplication.

    Returns:
        str: The resulting scaled point.
    """
    return compress(multiply(uncompress(element), scalar))


def combine(left_element: str, right_element: str) -> str:
    """
    Combines two BLS12-381 points using addition.

    Args:
        left_element (str): A compressed point.
        right_element (str): A compressed point.

    Returns:
        str: The resulting combined point.
    """
    return compress(add(uncompress(left_element), uncompress(right_element)))


def invert(element: str) -> str:
    """
    Calculates the inverse of a BLS12-381 point.

    Args:
        element (str): A compressed point.

    Returns:
        str: The resulting combined point.
    """
    return compress(neg(uncompress(element)))


def pair(g2_element: str, g1_element: str, final_exponentiate: bool = True) -> FQ12:
    """
    Compute the pairing operation on elliptic curve points represented as strings.

    Args:
        g2_element (str): A string representation of a point on G2 elliptic curve.
        g1_element (str): A string representation of a point on G1 elliptic curve.
        final_exponentiate (bool, optional): Whether to perform final exponentiation in the pairing computation. Defaults to True.

    Returns:
        FQ12: Result of the pairing operation as an element of the FQ12 field.
    """
    return pairing(uncompress(g2_element), uncompress(g1_element), final_exponentiate)


def hash_to_g2(message: str):
    """
    Generate a G2 point from a hex message string.

    Args:
        message (str): Hexadecimal string that represents a message.

    Returns:
        str: The compressed point as a hexadecimal string.
    """
    return compress(hash_to_G2(bytes.fromhex(message), "BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_".encode("utf-8"), hash_function()))


# identity elements
g1_identity = compress(Z1)
g2_identity = compress(Z2)

# Example usage:
if __name__ == "__main__":
    scalar = 123456789  # Example scalar value
    compressed_g1_point = g1_point(scalar)
    print(f"Compressed BLS12-381 g1 point: {compressed_g1_point}")
    uncompressed_g1_point = uncompress(compressed_g1_point)
    print(f"Uncompressed BLS12-381 g1 point: {uncompressed_g1_point}", uncompressed_g1_point[2])

    recompressed_g1_point = compress(uncompressed_g1_point)
    print(recompressed_g1_point == compressed_g1_point)

    g1 = g1_point(1)
    print("Invert g1", invert(g1))
    g_scaled = scale(g1, scalar)
    print(compressed_g1_point == g_scaled)

    compressed_g2_point = g2_point(scalar)
    print(f"Compressed BLS12-381 g2 point: {compressed_g2_point}")
    uncompressed_g2_point = uncompress(compressed_g2_point)
    print(f"Uncompressed BLS12-381 g2 point: {uncompressed_g2_point}", uncompressed_g2_point[2])

    recompressed_g2_point = compress(uncompressed_g2_point)
    print(recompressed_g2_point == compressed_g2_point)

    added_g1 = combine(g1, g1)
    print("Add g1 to g1", added_g1)
    print("g1 of 2", g1_point(2))
    print(added_g1 == g1_point(2))

    g2 = g2_point(1)
    print("Invert g2", invert(g2))
    added_g2 = combine(g2, g2)
    print("G2 Point", g2, len(g2))
    print(added_g2 == g2_point(2), '\n')

    u1g1 = g1_point(1)
    u2g1 = g1_point(2)
    v1g2 = g2_point(1)
    v2g2 = g2_point(2)
    print("e(U1+U2,V1)=e(U1,V1) x e(U2,V1)")
    pr = pair(v1g2, combine(u1g1, u2g1))
    pl = pair(v1g2, u1g1) * pair(v1g2, u2g1)
    print(pr == pl)

    print("e(U1,V1+V2)=e(U1,V1) x e(U1,V2)")
    pl = pair(combine(v1g2, v2g2), u1g1)
    pr = pair(v1g2, u1g1) * pair(v2g2, u1g1)
    print(pr == pl)

    print("e(aU,bV)=e(U,V)^(a*b)")
    a = 20
    b = 10
    au = scale(u1g1, a)
    bv = scale(v1g2, b)
    pl = pair(bv, au)
    pr = pair(v1g2, u1g1) ** (a * b)
    print(pr == pl)

    print("e(G,H)^k=1")
    print(pair(v1g2, u1g1) ** 0 == FQ12.one())
    print("e(Q,P)^(x^2 - x - 42)=1")
    print(pair(scale(v1g2, 7), scale(u1g1, 7)) * pair(invert(v1g2), scale(u1g1, 7)) * pair(invert(v1g2), scale(u1g1, 42)) == FQ12.one())
