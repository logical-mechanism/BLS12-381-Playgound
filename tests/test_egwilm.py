# ElGamal With An Invertible Linear Mapping (EGWILM)
#
# ElGamal can be replaced with Cramer-Shoup for CSWILM

import pytest
import random
import string
import time

from src.Registry import Registry
from src.reversible_mapping import map_to_point, string_to_int
from src.Registry.reversible_mapping import ReverseMapping


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


def test_alice_gives_to_bob():
    alice = Registry()
    bob = Registry()

    msg = "".join(
        random.choices(string.ascii_letters + string.digits + "+" + "/", k=47)
    )
    "/gETt53mvmuPXBJjBiVLmzyQ+MaskyfwJU9UdcHfeCHgD7x"

    alice_reverse_mapping_sig = alice.reverse_mapping_encryption(msg)

    # alice computes their randomized public value
    alice_r = alice_reverse_mapping_sig.c1 * alice.x
    # bob will need to apply their x to the c1 as an interactive process
    bob_r = alice_reverse_mapping_sig.c1 * bob.x
    w = bob_r + ~alice_r
    bob_c2 = alice_reverse_mapping_sig.c2 + w

    bob_reverse_mapping_sig = ReverseMapping(
        alice_reverse_mapping_sig.c1,
        bob_c2,
        alice_reverse_mapping_sig.h,
        alice_reverse_mapping_sig.o,
    )
    alice_message = alice_reverse_mapping_sig.extract(
        alice_reverse_mapping_sig.c1 * alice.x
    )
    print(alice_message)

    t0 = time.perf_counter()
    bob_message = bob_reverse_mapping_sig.extract(bob_reverse_mapping_sig.c1 * bob.x)
    elapsed = time.perf_counter() - t0
    print(elapsed, 192512 * elapsed / 60)
    print(bob_message)
    assert alice_reverse_mapping_sig.prove(alice_reverse_mapping_sig.c1 * alice.x)
    assert bob_reverse_mapping_sig.prove(bob_reverse_mapping_sig.c1 * bob.x)
    assert alice_message == bob_message
    assert alice_message == msg
