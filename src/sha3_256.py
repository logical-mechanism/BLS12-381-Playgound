from binascii import unhexlify
from hashlib import sha3_256


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
    concatenated_bytes = gb + grb + ub
    unhexed_bytes = unhexlify(concatenated_bytes)
    hash_result = sha3_256(unhexed_bytes).digest().hex()
    return hash_result


# Example usage:
if __name__ == "__main__":
    input_string = "Hello, world!"
    hash_digest = generate(input_string)
    print("SHA3-256 Hash:", hash_digest) 
    print(fiat_shamir_heuristic("", "", ""))
