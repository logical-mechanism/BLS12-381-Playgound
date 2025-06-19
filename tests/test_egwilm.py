# ElGamal With An Invertible Linear Mapping (EGWILM)
#
# ElGamal can be replaced with Cramer-Shoup @see test_cswilm.py
#
# EGWILM has delegation via proxy re-encryption (PRE)

import pytest
import random
import string

from src.Registry import Registry
from src.reversible_mapping import map_to_point, string_to_int, point_to_map
from src.Registry.reversible_mapping import ReverseMapping
from src.sha3_256 import generate, hash_to_int
from src.Registry.element import Element
from src.bls12_381 import g2_point, hash_to_g2, rng, pair



def test_simple_egwilm():
    alice = Registry()

    msg = "This is a secret message for Alice."
    print(string_to_int(msg))

    point, offset = map_to_point(msg)
    print(point, offset)

    alice_reverse_mapping_sig = alice.reverse_mapping_encryption(msg)
    print(alice_reverse_mapping_sig)

    message = alice_reverse_mapping_sig.extract(alice_reverse_mapping_sig.c1 * alice.x)
    print(message)

    assert alice_reverse_mapping_sig.prove(alice_reverse_mapping_sig.c1 * alice.x)
    assert message == msg


def test_message_too_long1():
    alice = Registry()
    msg = "This message will be too long to encrypt with egwilm."

    with pytest.raises(ValueError, match="Data too large to fit in field"):
        alice.reverse_mapping_encryption(msg)


def test_message_too_long2():
    msg = "This message will be too long for encryption pr"
    # purposely make it 1 byte less than the field modulus length
    # 1a0111ea397fe69a4b1ba7b6434bacd764774b84f38512bf6730d2a0f6b0f6241eabfffeb153ffffb9feffffffffaaab
    # 54686973206d6573736167652077696c6c20626520746f6f206c6f6e6720666f7220656e6372797074696f6e207072
    print(msg.encode("utf-8").hex())


def test_random_message():
    alice = Registry()
    # run 1000 tests and find some large off set for base64 string of length 47
    offsets = []
    for _ in range(1000):
        msg = "".join(
            random.choices(string.ascii_letters + string.digits + "+" + "/", k=47)
        )
        point, offset = map_to_point(msg)
        offsets.append(offset)
        # print(msg, offset)
    print(min(offsets), max(offsets))
    msg = "".join(
        random.choices(string.ascii_letters + string.digits + "+" + "/", k=47)
    )
    alice_reverse_mapping_sig = alice.reverse_mapping_encryption(msg)
    message = alice_reverse_mapping_sig.extract(alice_reverse_mapping_sig.c1 * alice.x)
    print(message)

    assert alice_reverse_mapping_sig.prove(alice_reverse_mapping_sig.c1 * alice.x)
    assert message == msg


def test_bob_cant_extract_or_decrypt():
    alice = Registry()
    bob = Registry()

    msg = "".join(
        random.choices(string.ascii_letters + string.digits + "+" + "/", k=47)
    )
    alice_reverse_mapping_sig = alice.reverse_mapping_encryption(msg)

    with pytest.raises(ValueError):
        alice_reverse_mapping_sig.extract(alice_reverse_mapping_sig.c1 * bob.x)

    with pytest.raises(UnicodeDecodeError):
        alice_reverse_mapping_sig.prove(alice_reverse_mapping_sig.c1 * bob.x)


def test_alice_and_bob_have_similar_messages():
    alice = Registry()
    bob = Registry()

    msg = "".join(
        random.choices(string.ascii_letters + string.digits + "+" + "/", k=47)
    )

    point, _ = map_to_point(msg)
    M = Element(point)
    r = rng()
    s = alice.u * r
    a_c2 = M + s

    w = rng()
    s = bob.u * w
    b_c2 = M + s

    # since alice knows r and w, a proof can be formed to bob that the message is the same as alice
    q = g2_point(1)
    q_r = g2_point(r)
    q_w = g2_point(w)

    assert pair(q_w, bob.u.value) * pair(q, a_c2.value) == pair(q_r, alice.u.value) * pair(q, b_c2.value)


def test_alice_gives_to_bob():
    alice = Registry()
    bob = Registry()

    msg = "".join(
        random.choices(string.ascii_letters + string.digits + "+" + "/", k=47)
    )

    alice_reverse_mapping_sig = alice.reverse_mapping_encryption(msg)
    # print(alice_reverse_mapping_sig)

    # now bob needs access so alice creates the shared key
    shared = alice.x * bob.u
    k = hash_to_int(shared.value)  # we need a hash to int function
    g_k = k * alice.g
    g_k = ~g_k  # inverse

    # use the shared key to change the c1 point
    # now bob has access to the encrypted message
    bob_reverse_mapping_sig = ReverseMapping(
        g_k + alice.x * alice_reverse_mapping_sig.c1,
        alice_reverse_mapping_sig.c2,
        alice_reverse_mapping_sig.h,
        alice_reverse_mapping_sig.o,
    )

    # now bob needs to decrypt the message
    shared = bob.x * alice.u
    k = hash_to_int(shared.value)
    g_k = k * bob.g
    w = g_k + bob_reverse_mapping_sig.c1
    w = ~w

    m = bob_reverse_mapping_sig.c2 + w
    bob_message = point_to_map(m.value, bob_reverse_mapping_sig.o)
    # print(bob_message)

    alice_message = alice_reverse_mapping_sig.extract(
        alice_reverse_mapping_sig.c1 * alice.x
    )
    # print(alice_message)

    assert alice_reverse_mapping_sig.prove(alice_reverse_mapping_sig.c1 * alice.x)
    assert alice_message == bob_message
    assert alice_message == msg
