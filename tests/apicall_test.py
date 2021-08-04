"""
Tests that use VCR to record responses

To record new tests simple delete the desired cassette
file from ./tests/fixtures and run the test suite.

NOTE: During recording this test suite requires an Auth
token to be present in a .env file stored in the project
root. Your username is also required

    USERNAME=[YOUR USERNAME]
    USERTOKEN=[YOUR AUTH TOKEN]
"""
import vcr
from egggist import EggGist
from secretbox import SecretBox


TEST_FILE = "test_file.md"
TEST_CONTENT = "# Test Gist"

CREATE_SUCCESS_CASSETE = "tests/fixtures/create_success.yaml"


secrets = SecretBox(auto_load=True)

gist_recorder = vcr.VCR(
    cassette_library_dir="tests/fixtures",
    record_mode="once",
    filter_headers=["Authorization"],
    match_on=["uri", "path"],
    serializer="yaml",
)


def test_gist_post() -> None:
    """Record a successful create of a gist"""
    gist_client = EggGist()
    gist_client.config.username = secrets.get("USERNAME")
    gist_client.config.usertoken = secrets.get("USERTOKEN")
    with gist_recorder.use_cassette(CREATE_SUCCESS_CASSETE):
        result = gist_client.post_gist(TEST_FILE, TEST_CONTENT)

    assert result is not None
