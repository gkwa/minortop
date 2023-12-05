import pytest

from minortop.skeleton import fib, main

__author__ = "Taylor Monacelli"
__copyright__ = "Taylor Monacelli"
__license__ = "MPL-2.0"


def test_fib():
    """API Tests"""
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)


def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["7"])
    captured = capsys.readouterr()
    assert "The 7-th Fibonacci number is 13" in captured.out


def test_main_with_verbose_flag(caplog):
    """Test CLI with verbose flag"""

    main(["--verbose", "5"])

    assert any("Script ends here" in record.message for record in caplog.records)


def test_main_with_very_verbose_flag(caplog):
    """Test CLI with verbose flag"""

    main(["--very-verbose", "5"])

    assert any(
        "Starting crazy calculations..." in record.message for record in caplog.records
    )
