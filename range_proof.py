from random import randrange

from src.bls import field_order
from src.range import generate, prove


def main():
    d = randrange(1, field_order - 1)
    print(f"Prove {d} exists between 1 and {field_order}")
    proof = generate(d)
    print("Range Proof:", proof)
    print("Is it valid?", prove(proof))


if __name__ == "__main__":
    main()
