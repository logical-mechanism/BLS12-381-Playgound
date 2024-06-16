# main.py
import copy
from random import randrange

from src.bls12_381 import field_order
from src.commitment import Commitment
from src.diffie_hellman_tuples import proveDHTuple
from src.range import Range
from src.Registry import Registry


def main():
    alice = Registry()
    print("Alice:", alice, '\n')

    print("Alice Inverse Public Element:", ~alice.u)

    alice_sig = alice.schnorr_signature()
    print("Alice Schnorr Signature:", alice_sig)
    print("Valid Signature?", alice_sig.prove(), '\n')

    msg = "The message to be signed."
    alice_msg_sig = alice.fiat_shamir_signature(msg)
    print("Alice Fiat Shamir Signature:", alice_msg_sig)
    print("Valid Signature?", alice_msg_sig.prove(), '\n')

    alice_elgamal_sig = alice.elgamal_encryption(msg)
    print("Alice ElGamal Signature:", alice_elgamal_sig)
    print("Valid Signature?", alice_elgamal_sig.prove(alice_elgamal_sig.c1 * alice.x), '\n')

    alice_random = copy.deepcopy(alice)
    y = alice.rng()
    alice_random.rerandomize(y)
    print("Alice Re-Randomized:", alice_random)
    alice_random_sig = alice_random.schnorr_signature()
    print("Alice Re-Randomized Schnorr Signature:", alice_random_sig)
    print("Valid Signature?", alice_random_sig.prove(), '\n')

    alice_random_msg_sig = alice_random.fiat_shamir_signature(msg)
    print("Alice Re-Randomized Fiat Shamir Signature:", alice_random_msg_sig)
    print("Valid Signature?", alice_random_msg_sig.prove(), '\n')

    outcome = proveDHTuple(y, alice, alice_random)
    print("Re-Randomized Valid:", outcome)

    d = randrange(1, field_order - 1)
    print(f"Prove {d} exists between 1 and {field_order}")
    range_proof = Range(d)
    print("Range Proof:", range_proof)
    print("Is it valid?", range_proof.prove(), '\n')

    print("Commitment:")
    v0 = 123456789
    v1 = 987654321
    c0 = Commitment(v0)
    c1 = Commitment(v1)
    print(c0)
    print(c1)
    print(c0 + c1)
    print(Commitment(0))
    print(Commitment(v0, 0))
    print(Commitment(0, 0))


if __name__ == "__main__":
    main()
