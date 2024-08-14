from random import randrange

import pytest

from src.bls12_381 import field_order
from src.range import Range


def test_valid_range():
    d = randrange(1, field_order - 1)
    r = Range(d)
    assert r.prove()


def test_age_verification_model_too_low():
    lower = 18
    upper = 25
    age = 17
    with pytest.raises(ValueError, match="Invalid range proof: W value must be greater than zero."):
        Range(secret_value=age, lower_bound=lower, upper_bound=upper)


def test_age_verification_model_too_high():
    lower = 18
    upper = 25
    age = 32
    with pytest.raises(ValueError, match="Invalid range proof: Y value must be greater than zero."):
        Range(secret_value=age, lower_bound=lower, upper_bound=upper)


def test_age_verification_model1():
    lower = 18
    upper = 25
    age = 21
    r = Range(secret_value=age, lower_bound=lower, upper_bound=upper)
    print(r)
    assert r.prove()


def test_age_verification_model2():
    lower = 20
    upper = 125  # oldest ever is 122
    age = 21
    r = Range(secret_value=age, lower_bound=lower, upper_bound=upper)
    assert r.prove()


def test_lower_range_value():
    with pytest.raises(ValueError, match="Invalid range proof: W value must be greater than zero."):
        Range(1)


def test_upper_range_value():
    with pytest.raises(ValueError, match="Invalid range proof: Y value must be greater than zero."):
        Range(field_order - 1)


if __name__ == "__main__":
    pytest.main()
