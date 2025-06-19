import pytest

from src.Relic import Relic


def test_alice_is_not_bob():
    alice = Relic()
    bob = Relic()
    assert alice != bob

def test_cramer_shoup_encryption():
    alice = Relic()
    print(alice)
    msg = "acabbeefcafe"
    alice_encryption = alice.encrypt(msg)
    print(alice_encryption)
    assert alice.prove(alice_encryption)
    message = alice.extract(alice_encryption)
    assert message == msg