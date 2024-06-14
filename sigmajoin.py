# main.py
import copy

from src.bls import rng
from src.diffie_hellman_tuples import proveDHTuple
from src.Registry import Registry


def mix_two():
    mixer = rng()

    alice = Registry()
    alice0 = copy.deepcopy(alice)
    alice0.rerandomize(mixer)

    bob = Registry()
    bob0 = copy.deepcopy(bob)
    bob0.rerandomize(mixer)

    alice_outcome = proveDHTuple(mixer, alice, alice0) or proveDHTuple(mixer, alice, bob0)
    print("Did Alice Mix?", alice_outcome)
    bob_outcome = proveDHTuple(mixer, bob, alice0) or proveDHTuple(mixer, bob, bob0)
    print("Did Bob Mix?", bob_outcome)


def mix_three():
    mixer = rng()

    alice = Registry()
    alice0 = copy.deepcopy(alice)
    alice0.rerandomize(mixer)

    bob = Registry()
    bob0 = copy.deepcopy(bob)
    bob0.rerandomize(mixer)

    carol = Registry()
    carol0 = copy.deepcopy(carol)
    carol0.rerandomize(mixer)

    alice_outcome = proveDHTuple(mixer, alice, alice0) or proveDHTuple(mixer, alice, bob0) or proveDHTuple(mixer, alice, carol0)
    print("Did Alice Mix?", alice_outcome)
    bob_outcome = proveDHTuple(mixer, bob, alice0) or proveDHTuple(mixer, bob, bob0) or proveDHTuple(mixer, bob, carol0)
    print("Did Bob Mix?", bob_outcome)
    carol_outcome = proveDHTuple(mixer, carol, alice0) or proveDHTuple(mixer, carol, bob0) or proveDHTuple(mixer, carol, carol0)
    print("Did Carol Mix?", carol_outcome)


def mix_arbitrary():
    n = 25
    mixer = rng()

    users = [Registry() for _ in range(n)]
    users_copy = [copy.deepcopy(user) for user in users]

    for user in users_copy:
        user.rerandomize(mixer)

    for user in users:
        print("Did User Mix?", user)
        print(any([proveDHTuple(mixer, user, user_copy)] for user_copy in users_copy))


if __name__ == "__main__":
    print("Mix Two")
    mix_two()

    print("\nMix Three")
    mix_three()

    print("\nMix Arbitrary")
    mix_arbitrary()
