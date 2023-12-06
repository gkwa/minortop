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
