"""Tests for __main__.py"""
from typing import Any
from unittest.mock import MagicMock
from unittest.mock import patch

from egggist import __main__ as main

CLI_LINE = [
    "--debug",
    "--private",
    "--set-username",
    "mockuser",
    "--set-token",
    "mocktoken",
    "mockfile.txt",
    "mockfile.json",
]

CLI_EXPECTED = {
    "debug": True,
    "private": True,
    "name": "mockuser",
    "token": "mocktoken",
    "filename": ["mockfile.txt", "mockfile.json"],
}


def test_cli_parser() -> None:
    """CLI test"""

    args = main.cli_parser(CLI_LINE)

    for key, value in CLI_EXPECTED.items():
        arg = getattr(args, key)

        assert arg == value, f"Arg attrib: {key}"


def test_main_nothing_to_do(capfd: Any) -> None:
    """Do nothing if nothing to do"""
    args = main.cli_parser([])
    with patch.object(main, "cli_parser", MagicMock(return_value=args)):
        main.main()
        out, _ = capfd.readouterr()

    assert out == main.NOTHING_TO_DO + "\n"


def test_main_success(capfd: Any) -> None:
    """Full success"""
    args = main.cli_parser(CLI_LINE)
    post_gist = MagicMock(return_value=MagicMock(html_url="mockurl"))
    client = MagicMock(post_gist=post_gist)

    with patch.object(main, "cli_parser", MagicMock(return_value=args)):
        with patch.object(main, "EggGist", MagicMock(return_value=client)):

            main.main()

            out, _ = capfd.readouterr()

    assert main.SUCCESS in out
    assert "mockurl" in out


def test_main_failure(capfd: Any) -> None:
    """Full failure"""
    args = main.cli_parser(CLI_LINE)
    post_gist = MagicMock(return_value=None)
    client = MagicMock(post_gist=post_gist)

    with patch.object(main, "cli_parser", MagicMock(return_value=args)):
        with patch.object(main, "EggGist", MagicMock(return_value=client)):

            main.main()

            out, _ = capfd.readouterr()

    assert main.FAILURE in out
