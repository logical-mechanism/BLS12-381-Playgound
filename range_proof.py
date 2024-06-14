from random import randrange

from src.bls import field_order
from src.range import Range


def main():
    d = randrange(1, field_order - 1)
    print(f"Prove {d} exists between 1 and {field_order}")
    range_proof = Range(d)
    print("Range Proof:", range_proof)
    print("Is it valid?", range_proof.prove())


if __name__ == "__main__":
    main()
