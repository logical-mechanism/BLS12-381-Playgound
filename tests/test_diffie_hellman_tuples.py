import copy

import pytest

from src.diffie_hellman_tuples import proveDHTuple
from src.Registry.registry import Registry


def test_prove_DHTuple():
    alice = Registry()
    alice_random = copy.deepcopy(alice)
    y = alice.rng()
    alice_random.rerandomize(y)
    outcome = proveDHTuple(y, alice, alice_random)
    assert outcome


def test_self_prove_DHTuple_is_false():
    alice = Registry()
    y = alice.rng()
    outcome = proveDHTuple(y, alice, alice)
    assert outcome is False


def test_mix_prove_DHTuple_is_false():
    alice = Registry()
    bob = Registry()
    y = alice.rng()
    outcome = proveDHTuple(y, alice, bob)
    assert outcome is False


if __name__ == "__main__":
    pytest.main()
