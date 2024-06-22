from random import randrange

import pytest

from src.bls12_381 import field_order
from src.range import Range


def test_valid_range():
    d = randrange(1, field_order - 1)
    r = Range(d)
    assert r.prove()


if __name__ == "__main__":
    pytest.main()
