from src.value import Value


def test_empty_equals_empty():
    assert Value({}) == Value({})


def test_lovelace_equals_lovelace():
    assert Value({"": {"": 1}}) == Value({"": {"": 1}})


def test_mixed_equals_mixed():
    assert Value({"": {"": 1}, "acab": {"beef": 1, "face": 1}}) == Value({"": {"": 1}, "acab": {"beef": 1, "face": 1}})


def test_not_equal_values():
    assert Value({"": {"": 0}}) != Value({"": {"": 1}})


def test_remove_mixed_zeros():
    result = Value({"": {"": 0}, "acab": {"beef": 1, "face": 0}})
    answer = Value({"acab": {"beef": 1}})
    result._remove_zero_entries()
    assert result == answer


def test_remove_multiple_zeros():
    result = Value({"": {"": 0}, "acab": {"face": 0}})
    answer = Value({})
    result._remove_zero_entries()
    assert result == answer


def test_remove_single_zero():
    result = Value({"": {"": 0}})
    answer = Value({})
    result._remove_zero_entries()
    assert result == answer


def test_negate_positive_value():
    result = Value({"": {"": 1}})
    answer = Value({"": {"": -1}})
    result.negate()
    assert result == answer


def test_negate_negative_value():
    result = Value({"": {"": -1}})
    answer = Value({"": {"": 1}})
    result.negate()
    assert result == answer


def test_add_values_equal_to_zero():
    result = Value({"": {"": -1}}) + Value({"": {"": 1}})
    answer = Value({})
    assert result == answer


def test_sub_values_equal_to_zero():
    result = Value({"": {"": 1}}) - Value({"": {"": 1}})
    answer = Value({})
    assert result == answer


def test_add_zero_to_zero():
    result = Value({}) + Value({})
    answer = Value({})
    assert result == answer


def test_sub_zero_to_zero():
    result = Value({}) - Value({})
    answer = Value({})
    assert result == answer


def test_sub_value_from_zero():
    result = Value({}) - Value({"": {"": 1}})
    answer = Value({"": {"": -1}})
    assert result == answer


def test_mul_by_zero():
    result_r = 0 * Value({"": {"": 1}})
    result_l = Value({"": {"": 1}}) * 0
    answer = Value({})
    assert result_r == answer
    assert result_l == answer


def test_mul_by_one():
    result_r = 1 * Value({"": {"": 1}})
    result_l = Value({"": {"": 1}}) * 1
    answer = Value({"": {"": 1}})
    assert result_r == answer
    assert result_l == answer
