# main.py
import copy

from src.diffie_hellman_tuples import proveDHTuple
from src.Registry import Registry


def main():
    alice = Registry()
    alice_sig = alice.schnorr_signature()
    print("Alice:", alice)
    print("Alice Schnorr Signature:", alice_sig)
    print("Valid Signature?", alice_sig.prove(), '\n')

    msg = "The message to be signed."
    alice_msg_sig = alice.fiat_shamir_signature(msg)
    print("Alice Fiat Shamir Signature:", alice_msg_sig)
    print("Valid Signature?", alice_msg_sig.prove(), '\n')

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


if __name__ == "__main__":
    main()
