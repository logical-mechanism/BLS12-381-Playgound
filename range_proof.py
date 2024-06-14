from src.range import generate, prove


def main():
    d = 563634634634634634634
    print(f"Prove {d} exists between 1 and p")
    proof = generate(d)
    print("Range Proof:", proof)
    print("Is it valid?", prove(proof))


if __name__ == "__main__":
    main()
