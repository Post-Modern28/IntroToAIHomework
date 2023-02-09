import pytest

from With_files.ML_test import f


def test1():
    assert f(3) == 6


def test2():
    assert f(4) == 8


def test3():
    assert f(5) == 10


if __name__ == "__main__":
    pytest.main()
