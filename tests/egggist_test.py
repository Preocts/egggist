"""Tests for egggist.py"""
import json
import os
import tempfile
from pathlib import Path
from typing import Generator
from unittest.mock import patch

import pytest
from egggist import EggGist
from egggist import egggist


MOCK_CONFIG = {"username": "TEST", "usertoken": "TOKEN"}
NO_FILE_NAMED_THIS = "this_file_should_not_exist"


@pytest.fixture(scope="function", name="config_file")
def fixture_config_file() -> Generator[str, None, None]:
    """Creates a config file and returns the path"""
    try:
        file_desc, path = tempfile.mkstemp()
        with os.fdopen(file_desc, "w", encoding="utf-8") as temp_file:
            json.dump(MOCK_CONFIG, temp_file)
        yield path
    finally:
        os.remove(path)


def test_create_instance_with_config(config_file: str) -> None:
    """Constructor loads config"""
    with patch.object(EggGist, "CONFIG_FILE", config_file):
        gist_client = EggGist()

    assert gist_client.config.as_dict() == MOCK_CONFIG


def test_create_instance_without_config() -> None:
    """Load without config to later prompt for values"""
    assert not Path(NO_FILE_NAMED_THIS).exists()
    with patch.object(EggGist, "CONFIG_FILE", NO_FILE_NAMED_THIS):
        gist_client = EggGist()

    for value in gist_client.config.as_dict().values():
        assert value is None


def test_configfile_class() -> None:
    """Data model for holding config"""

    config = egggist.ConfigFile.from_dict(MOCK_CONFIG)
    config_empty = egggist.ConfigFile.from_dict({})

    for key, value in MOCK_CONFIG.items():
        assert getattr(config, key) == value
        assert getattr(config_empty, key) is None

    assert config.as_dict() == MOCK_CONFIG
