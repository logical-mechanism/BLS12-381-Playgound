import pytest

from src.Registry import Registry
from src.Registry.util import hex_encode


def test_alice_is_not_bob():
    alice = Registry()
    bob = Registry()
    assert alice != bob


def test_schnorr_signature():
    alice = Registry()
    alice_sig = alice.schnorr_signature()
    assert alice_sig.prove()

    alice.rerandomize()
    alice_sig = alice.schnorr_signature()
    assert alice_sig.prove()


def test_fiat_shamir_signature():
    alice = Registry()
    msg = "The message to be signed."
    alice_msg_sig = alice.fiat_shamir_signature(msg)
    assert alice_msg_sig.prove()

    alice.rerandomize()
    alice_msg_sig = alice.fiat_shamir_signature(msg)
    assert alice_msg_sig.prove()


def test_elgamal_encryption():
    alice = Registry()
    msg = "The message to be signed."
    alice_elgamal_sig = alice.elgamal_encryption(msg)
    assert alice_elgamal_sig.prove(alice_elgamal_sig.c1 * alice.x)


def test_reverse_mapping_encryption1():
    alice = Registry()
    msg = "The message to be signed."
    alice_reverse_mapping_sig = alice.reverse_mapping_encryption(msg)
    message = alice_reverse_mapping_sig.extract(alice_reverse_mapping_sig.c1 * alice.x)
    assert alice_reverse_mapping_sig.prove(alice_reverse_mapping_sig.c1 * alice.x)
    assert message == msg


def test_reverse_mapping_encryption2():
    alice = Registry()
    msg = "ffffffffffffffffffffffffffffffffffffffffffffff"
    alice_reverse_mapping_sig = alice.reverse_mapping_encryption(msg)
    message = alice_reverse_mapping_sig.extract(alice_reverse_mapping_sig.c1 * alice.x)
    assert alice_reverse_mapping_sig.prove(alice_reverse_mapping_sig.c1 * alice.x)
    assert message == msg


def test_reverse_mapping_encryption3():
    alice = Registry()
    msg = "The length 32 string is a secret"
    alice_reverse_mapping_sig = alice.reverse_mapping_encryption(msg)
    message = alice_reverse_mapping_sig.extract(alice_reverse_mapping_sig.c1 * alice.x)
    assert alice_reverse_mapping_sig.prove(alice_reverse_mapping_sig.c1 * alice.x)
    assert message == msg


def test_reverse_mapping_a_value():
    alice = Registry()
    value = 44203
    msg = hex(value)[2:]
    alice_reverse_mapping_sig = alice.reverse_mapping_encryption(msg)
    message = alice_reverse_mapping_sig.extract(alice_reverse_mapping_sig.c1 * alice.x)
    assert int(message, 16) == value


def test_reverse_mapping_a_value2():
    alice = Registry()
    value = 45 * pow(10, 9) * pow(10, 6)
    msg = hex(value)[2:]
    alice_reverse_mapping_sig = alice.reverse_mapping_encryption(msg)
    print(alice_reverse_mapping_sig)
    message = alice_reverse_mapping_sig.extract(alice_reverse_mapping_sig.c1 * alice.x)
    assert int(message, 16) == value


def test_boneh_lynn_shacham_signature():
    alice = Registry()
    msg1 = "The first message to be signed."
    msg2 = "The second message to be signed."
    alice_bls_sig1 = alice.boneh_lynn_shacham_signature(hex_encode(msg1))
    alice_bls_sig2 = alice.boneh_lynn_shacham_signature(hex_encode(msg2))
    assert alice_bls_sig1.prove()
    alice_bls_aggregate = alice_bls_sig1 + alice_bls_sig2
    assert alice_bls_aggregate.prove()

def test_cramer_shoup_encryption():
    alice = Registry()
    msg = "acabbeefcafe"
    alice_cramer_shoup_sig = alice.cramer_shoup_encryption(msg)
    print(alice_cramer_shoup_sig)
    assert alice_cramer_shoup_sig.prove(alice.x)
    message = alice_cramer_shoup_sig.extract(alice.x)
    assert message == msg

if __name__ == "__main__":
    pytest.main()
