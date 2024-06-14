import secrets

from py_ecc.bls import G2ProofOfPossession as bls
from py_ecc.bls.g2_primitives import G1_to_pubkey, pubkey_to_G1
from py_ecc.optimized_bls12_381 import add, multiply, neg

field_order = 52435875175126190479447740508185965837690552500527637822603658699938581184513


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


def point(scalar: int) -> str:
    """
    Generates a BLS12-381 point from the G1 generator using scalar multiplication
    and returns it in compressed format.

    Args:
        scalar (int): The scalar value for multiplication.

    Returns:
        bytes: The resulting BLS12-381 point in compressed format.
    """
    pk = bls.SkToPk(scalar)
    pk_bytes = pk
    pk_hex = pk_bytes.hex()
    return pk_hex


def uncompress(hex_str: str) -> tuple:
    """
    Uncompresses a hexadecimal string to a BLS12-381 G1 point.

    Args:
        hex_str (str): The compressed G1 point as a hexadecimal string.

    Returns:
        tuple: The uncompressed G1 point.
    """
    return pubkey_to_G1(bytes.fromhex(hex_str))


def compress(g1_element: tuple) -> str:
    """
    Compresses a BLS12-381 G1 point to a hexadecimal string.

    Args:
        g1_element (tuple): The G1 point to be compressed.

    Returns:
        str: The compressed G1 point as a hexadecimal string.
    """
    return G1_to_pubkey(g1_element).hex()


def scale(g1_element: str, scalar: int) -> str:
    """
    Scales a BLS12-381 G1 point by a given scalar using scalar multiplication.

    Args:
        g1_element (str): The compressed G1 point to be scaled.
        scalar (int): The scalar value for multiplication.

    Returns:
        str: The resulting scaled G1 point.
    """
    element = uncompress(g1_element)
    return compress(multiply(element, scalar))


def combine(left_element: str, right_element: str) -> str:
    """
    Combines two BLS12-381 G1 points using addition.

    Args:
        left_element (str): A compressed G1 point.
        right_element (str): A compressed G1 point.

    Returns:
        str: The resulting combined G1 point.
    """
    lelement = uncompress(left_element)
    relement = uncompress(right_element)
    return compress(add(lelement, relement))


def invert(g1_element: str) -> str:
    """
    Calculates the inverse of aBLS12-381 G1 point.

    Args:
        g1_element (str): A compressed G1 point.

    Returns:
        str: The resulting combined G1 point.
    """
    element = uncompress(g1_element)
    return compress(neg(element))


# Example usage:
if __name__ == "__main__":
    scalar = 123456789  # Example scalar value
    compressed_point = point(scalar)
    print(f"Compressed BLS12-381 point: {compressed_point}")
    uncompressed = uncompress(compressed_point)
    recompressed = compress(uncompressed)
    print(recompressed == compressed_point)

    g1 = point(1)
    g_scaled = scale(g1, scalar)
    print(compressed_point == g_scaled)

    hex_string = rng()
    print(f"Generated hex string: {hex_string}")

    added_g1 = combine(g1, g1)
    print(added_g1 == point(2))
