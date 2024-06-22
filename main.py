# main.py
import copy

from src.Registry import Registry
from src.Registry.util import hex_encode


def main():
    alice = Registry()
    print("Alice:", alice, '\n')
    bob = Registry()
    print("Bob:", bob, '\n')

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

    msg1 = "The first message to be signed."
    msg2 = "The second message to be signed."

    alice_bls_sig1 = alice.boneh_lynn_shacham_signature(hex_encode(msg1))
    alice_bls_sig2 = alice.boneh_lynn_shacham_signature(hex_encode(msg2))
    print("Alice BLS Signature:", alice_bls_sig1)
    print("Valid Signature?", alice_bls_sig1.prove(), '\n')
    alice_bls_aggregate = alice_bls_sig1 + alice_bls_sig2
    print("Alice BLS Aggregate Signature:", alice_bls_aggregate)
    print("Valid Signature?", alice_bls_aggregate.prove(), '\n')

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


if __name__ == "__main__":
    main()
