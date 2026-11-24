import pytest

from cachegraph import fingerprint


def test_same_input_produces_same_fingerprint():
    first = fingerprint({"name": "Falah", "age": 21})
    second = fingerprint({"name": "Falah", "age": 21})

    assert first == second


def test_dictionary_order_does_not_matter():
    first = fingerprint({"name": "Falah", "age": 21})
    second = fingerprint({"age": 21, "name": "Falah"})

    assert first == second


def test_different_inputs_produce_different_fingerprints():
    first = fingerprint({"user_id": 10})
    second = fingerprint({"user_id": 20})

    assert first != second


def test_boolean_and_integer_are_different():
    assert fingerprint(True) != fingerprint(1)


def test_list_and_tuple_are_different():
    assert fingerprint([1, 2]) != fingerprint((1, 2))


def test_nested_structures():
    first = fingerprint({
        "user": {
            "id": 10,
            "roles": ["admin", "editor"]
        }
    })

    second = fingerprint({
        "user": {
            "id": 10,
            "roles": ["admin", "editor"]
        }
    })

    assert first == second


def test_bytes_are_supported():
    assert fingerprint(b"hello") == fingerprint(b"hello")
    assert fingerprint(b"hello") != fingerprint(b"world")


def test_unsupported_types_are_rejected():
    with pytest.raises(TypeError):
        fingerprint({1, 2, 3})


def test_non_string_dictionary_keys_are_rejected():
    with pytest.raises(TypeError):
        fingerprint({1: "value"})


def test_non_finite_floats_are_rejected():
    with pytest.raises(ValueError):
        fingerprint(float("nan"))
