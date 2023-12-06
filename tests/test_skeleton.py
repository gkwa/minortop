import pytest

import minortop.main


def test_main_with_version_option(capsys):
    """Test CLI with version option"""
    with pytest.raises(SystemExit) as e:
        minortop.main.main(["--version"])

    # Check if the exit status is 0
    assert e.value.code == 0

    # Optionally, you can also check the captured output
    captured = capsys.readouterr()
    assert "minortop" in captured.out.strip()


def test_main_with_no_arguments(capsys, monkeypatch):
    """Test CLI with no arguments (show help)"""
    # Mock the setup_logging function to avoid unnecessary logs during testing
    monkeypatch.setattr(minortop.main, "setup_logging", lambda x: None)

    result = minortop.main.main([])
    captured = capsys.readouterr()

    # Check if the exit status is 1 (indicating an error)
    assert (
        "Just a command, sub command, subsub command demonstration"
        in captured.out.strip()
    )
    assert result == 1


def test_main_with_invalid_argument(capsys, monkeypatch):
    """Test CLI with no arguments (show help)"""
    with pytest.raises(SystemExit) as e:
        minortop.main.main(["garbage"])

    assert e.value.code == 2

    # Optionally, you can also check the captured output
    captured = capsys.readouterr()
    assert "invalid choice:" in captured.err.strip()


def test_main_with_multiple_invalid_arguments(capsys, monkeypatch):
    """Test CLI with no arguments (show help)"""
    with pytest.raises(SystemExit) as e:
        minortop.main.main(["garbage", "garbage"])

    assert e.value.code == 2

    # Optionally, you can also check the captured output
    captured = capsys.readouterr()
    assert "invalid choice:" in captured.err.strip()
