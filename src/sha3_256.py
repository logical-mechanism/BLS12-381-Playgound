from binascii import unhexlify
from hashlib import sha3_256


def hash_function():
    return sha3_256


def generate(input_string: str) -> str:
    """
    Calculates the SHA3-256 hash digest of the input string.

    Args:
        input_string (str): The string to be hashed.

    Returns:
        str: The SHA3-256 hash digest of the input string.
    """
    # Encode the input string to bytes before hashing
    encoded_string = input_string.encode('utf-8')

    # Calculate the hash digest using SHA3-256
    hash_digest = sha3_256(encoded_string).hexdigest()

    return hash_digest


def fiat_shamir_heuristic(gb: str, grb: str, ub: str) -> str:
    """
    Applies the Fiat-Shamir heuristic to generate a hash.

    Parameters:
    gb (str): The first input string, typically representing a value in hex.
    grb (str): The second input string, typically representing a value in hex.
    ub (str): The third input string, typically representing a value in hex.

    Returns:
    str: The resulting hash as a hexadecimal string.
    """
    # Concatenate the input strings
    concatenated_bytes = gb + grb + ub

    # Convert the concatenated hex string to bytes
    unhexed_bytes = unhexlify(concatenated_bytes)

    # Compute the SHA-3 (256-bit) hash of the bytes and convert to a hex string
    hash_result = sha3_256(unhexed_bytes).digest().hex()

    return hash_result


# Example usage:
if __name__ == "__main__":
    input_string = "Hello, world!"
    hash_digest = generate(input_string)
    print("SHA3-256 Hash:", hash_digest)
    print(fiat_shamir_heuristic("", "", ""))
