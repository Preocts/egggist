"""
Tool: Record responses of creating a gist for unit test use
"""
import json
import pathlib
from typing import Dict
from typing import NamedTuple

from egggist.egggist import EggGist

FILE_PATH = "tests/fixtures"
FILE_SUCCESS = "create_success.json"
FILE_FAIL = "create_fail_token.json"

TEST_FILE = "test_file.md"
TEST_CONTENT = "# Test Gist"


class Secrets(NamedTuple):
    """Hold our secrets"""

    username: str
    usertoken: str


def build_client() -> EggGist:
    """Fixture of our client"""
    if not pathlib.Path(".env").exists():
        raise FileNotFoundError("'.env' file required, check module docstring")

    input_file = open(".env", "r", encoding="utf-8").read()
    secrets = Secrets(**load_secrets(input_file))

    gist_client = EggGist()
    gist_client.config.username = secrets.username
    gist_client.config.usertoken = secrets.usertoken

    return gist_client


def load_secrets(input_file: str) -> Dict[str, str]:
    """Parses env file for required values"""
    values: Dict[str, str] = {}
    for line in input_file.split("\n"):
        if not line or line.strip().startswith("#") or len(line.split("=", 1)) != 2:
            continue
        key, value = line.split("=", 1)

        values[key.strip().lower()] = value
    return values


def record_successful_create() -> None:
    """Record success"""
    filepath = pathlib.Path(FILE_PATH, FILE_SUCCESS)
    if filepath.exists():
        print(f"Skipping 'record_successful_create, file exists: {filepath}")
        return

    gist_client = build_client()

    result = gist_client.post_gist(TEST_FILE, TEST_CONTENT)

    open(filepath, "w").write(json.dumps(result, indent=4))


def record_fail_create_token() -> None:
    """Record failure due to token"""
    filepath = pathlib.Path(FILE_PATH, FILE_FAIL)
    if filepath.exists():
        print(f"Skipping 'record_fail_create_token, file exists: {filepath}")
        return

    gist_client = build_client()

    gist_client.config.usertoken = "notatoken"

    result = gist_client.post_gist(TEST_FILE, TEST_CONTENT)

    open(filepath, "w").write(json.dumps(result, indent=4))


if __name__ == "__main__":
    if not pathlib.Path(FILE_PATH).exists():
        raise ValueError(f"Missing '{FILE_PATH}' path")

    record_successful_create()
    record_fail_create_token()
