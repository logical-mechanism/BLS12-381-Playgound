from src.bls import field_order, point
from src.Registry.element import Element


def prove(range_proof: dict) -> bool:
    """
    Verifies the correctness of a range proof.

    Parameters:
    range_proof (dict): A dictionary containing the components of the range proof.

    Returns:
    bool: True if the range proof is valid, False otherwise.
    """
    # Extract the components of the range proof from the dictionary
    A = range_proof["a"]
    B = range_proof["b"]
    D = range_proof["d"]
    Y = range_proof["y"]
    W = range_proof["w"]

    # Check the validity of the range proof by verifying the provided equations
    return A == B + Y + W and A + B + W == 2 * D + Y


def generate(d: int, a: int = field_order - 1, b: int = 1) -> dict:
    """
    Generates a range proof dictionary based on the provided values.

    Parameters:
    d (int): The value to be used in the range proof.
    a (int): The starting value for the range proof (default is field_order - 1).
    b (int): The ending value for the range proof (default is 1).

    Returns:
    dict: A dictionary containing the components of the range proof.
    """
    # Calculate y and w based on the provided values
    y = a - d
    w = d - b

    # Return a dictionary containing the elements of the range proof
    return {
        'a': Element(point(a)),
        'b': Element(point(b)),
        'd': Element(point(d)),
        'y': Element(point(y)),
        'w': Element(point(w)),
    }
