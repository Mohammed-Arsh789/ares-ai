from tools.calculator import calculate


def test_addition():

    assert calculate("2 + 3") == 5


def test_multiplication():

    assert calculate("10 * 5") == 50


def test_power():

    assert calculate("2 ** 3") == 8