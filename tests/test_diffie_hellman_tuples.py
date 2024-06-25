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


def test_twice_rerandomized_is_false():
    alice = Registry()
    alice_random = copy.deepcopy(alice)
    alice.rerandomize()
    y = alice.rng()
    alice_random.rerandomize(y)
    outcome = proveDHTuple(y, alice, alice_random)
    assert outcome is False


def test_mix_prove_DHTuple_is_false():
    alice = Registry()
    bob = Registry()
    y = alice.rng()
    outcome = proveDHTuple(y, alice, bob)
    assert outcome is False


def test_sigma_statement():
    alice = Registry()
    bob = Registry()
    y = alice.rng()
    alice_random = copy.deepcopy(alice)
    alice_random.rerandomize(y)
    bob_random = copy.deepcopy(bob)
    bob_random.rerandomize(y)
    alice_outcome = proveDHTuple(y, alice, alice_random) or proveDHTuple(y, alice, bob_random)
    bob_outcome = proveDHTuple(y, bob, alice_random) or proveDHTuple(y, bob, bob_random)
    assert alice_outcome
    assert bob_outcome


if __name__ == "__main__":
    pytest.main()
