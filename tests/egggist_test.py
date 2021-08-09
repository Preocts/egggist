"""Tests for egggist.py"""
import json
import os
import tempfile
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from egggist import EggGist
from egggist import egggist


MOCK_CONFIG = {"username": "TEST", "usertoken": "TOKEN"}
NO_FILE_NAMED_THIS = "this_file_should_not_exist"
CREATE_SUCCESS = open("tests/fixtures/create_success.json", "r").read().encode("utf-8")
CREATE_FAIL = open("tests/fixtures/create_fail_token.json", "r").read().encode("utf-8")


@pytest.fixture(scope="function", name="empty_file")
def fixture_empty_file() -> Generator[str, None, None]:
    """Creates an empty temp file and returns path"""
    try:
        file_desc, path = tempfile.mkstemp()
        os.close(file_desc)
        yield path
    finally:
        os.remove(path)


@pytest.fixture(scope="function", name="config_file")
def fixture_config_file(empty_file: str) -> Generator[str, None, None]:
    """Creates a config file and returns the path"""
    with open(empty_file, "w", encoding="utf-8") as temp_file:
        json.dump(MOCK_CONFIG, temp_file, indent=4)

    yield empty_file


@pytest.fixture(scope="function", name="client")
def fixture_client(config_file: str) -> Generator[EggGist, None, None]:
    """Gererate a client with config values mocked"""
    with patch.object(EggGist, "CONFIG_FILE", config_file):
        client = EggGist(check_config=False)

        yield client


def test_create_instance_with_config(config_file: str) -> None:
    """Constructor loads config"""
    with patch.object(EggGist, "CONFIG_FILE", config_file):
        gist_client = EggGist()

    assert gist_client.config.as_dict() == MOCK_CONFIG


def test_create_instance_without_config() -> None:
    """Load without config to later prompt for values"""
    assert not Path(NO_FILE_NAMED_THIS).exists()

    with patch("builtins.input", lambda value: "missing"):
        with patch.object(EggGist, "CONFIG_FILE", NO_FILE_NAMED_THIS):
            gist_client = EggGist()

        for value in gist_client.config.as_dict().values():
            assert value == "missing"


def test_create_instance_invalid_config(empty_file: str) -> None:
    """Load with invalid(empty) config"""

    with patch("builtins.input", lambda value: "missing"):
        with patch.object(EggGist, "CONFIG_FILE", empty_file):
            gist_client = EggGist()

        for value in gist_client.config.as_dict().values():
            assert value == "missing"


def test_configfile_class() -> None:
    """Data model for holding config"""

    config = egggist.ConfigFile.from_dict(MOCK_CONFIG)
    config_empty = egggist.ConfigFile.from_dict({})

    for key, value in MOCK_CONFIG.items():
        assert getattr(config, key) == value
        assert getattr(config_empty, key) is None

    assert config.as_dict() == MOCK_CONFIG


def test_build_headers_missing(client: EggGist) -> None:
    """Prompt for user input and use those values"""
    client.config.username = None
    client.config.usertoken = None

    headers = client._build_headers()

    assert headers["User-Agent"] == ""
    assert headers["Authorization"] == "token "


def test_build_headers_present(client: EggGist) -> None:
    """Do not prompt for input if config values are present"""

    headers = client._build_headers()

    assert headers["User-Agent"] == MOCK_CONFIG["username"]
    assert MOCK_CONFIG["usertoken"] in headers["Authorization"]


def test_post_gist_success(client: EggGist) -> None:
    """Use mock response to simulate success"""
    json_expected = json.loads(CREATE_SUCCESS.decode("utf-8"))
    with patch.object(client, "conn") as conn:
        read = MagicMock(return_value=CREATE_SUCCESS)
        response = MagicMock(status=201, read=read)
        conn.getresponse = MagicMock(return_value=response)

        client.files.append(egggist.File("test.md", "#"))

        results = client.post_gist()

        assert results is not None
        assert results.as_dict == json_expected


def test_post_no_files(client: EggGist) -> None:
    """No files should return None, no mocking needed"""
    result = client.post_gist()

    assert result is None


def test_post_gist_fail(client: EggGist) -> None:
    """Use mock to simulate a failed response"""
    with patch.object(client, "conn") as conn:
        read = MagicMock(return_value=CREATE_FAIL)
        response = MagicMock(status=403, read=read)
        conn.getresponse = MagicMock(return_value=response)

        client.files.append(egggist.File("test.md", "#"))

        results = client.post_gist()

        assert results is None


def test_save_config(client: EggGist, config_file: str) -> None:
    """Save config with different values"""
    expect_username = "save_test"
    expect_usertoken = "SAVE_TEST"

    client.config.username = expect_username
    client.config.usertoken = expect_usertoken

    client._save_config()

    result = client._load_config()

    assert result.username == expect_username
    assert result.usertoken == expect_usertoken


def test_add_file(client: EggGist, config_file: str) -> None:
    """Add a file to be posted"""
    client.add_file(config_file)

    assert client.files[-1].name == Path(config_file).name
    assert client.files[-1].content == json.dumps(MOCK_CONFIG, indent=4)
