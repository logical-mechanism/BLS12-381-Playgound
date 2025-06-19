# Cramer-Shoup With An Invertible Linear Mapping (CSWILM)
#
#

import pytest
import random
import string

from src.Relic import Relic

def random_string() -> str:
    msg = "".join(
        random.choices(string.ascii_letters + string.digits + "+" + "/", k=47)
    )
    return msg


def test_simple_cswilm():
    alice = Relic()
    msg = random_string()
    alice_encryption = alice.encrypt(msg)
    message = alice.extract(alice_encryption)
    assert alice.prove(alice_encryption)
    assert message == msg

def test_bob_cant_extract_or_decrypt():
    alice = Relic()
    bob = Relic()

    msg = random_string()
    alice_encryption = alice.encrypt(msg)
    
    with pytest.raises(ValueError):
        bob.extract(alice_encryption)

    assert bob.prove(alice_encryption) == False
