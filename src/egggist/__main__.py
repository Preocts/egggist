"""
Point of entry for CLI control

Author: Preocts
Discord: Preocts#8196
Repo: https://github.com/preocts/egggist
"""
import argparse
import logging
from typing import Optional
from typing import Sequence

from egggist.egggist import EggGist

REPO_URL = "https://github.com/preocts/egggist"
NOTHING_TO_DO = "Nothing to do."
SUCCESS = "Gist Created:"
FAILURE = "Something went wrong. Run with --debug for more details."


def cli_parser(args: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Configure argparse"""
    parser = argparse.ArgumentParser(
        prog="prfiles",
        description="Send a file to your GitHub Gist.",
        epilog=f"Check it. {REPO_URL}",
    )
    parser.add_argument(
        "filename",
        type=str,
        nargs="*",
        help="One, or more, files to be added to the gist (utf-8 encoding)",
    )
    parser.add_argument(
        "--set-username",
        type=str,
        dest="name",
        help="Store your username in '~/.egggist_conf",
    )
    parser.add_argument(
        "--set-token",
        type=str,
        dest="token",
        help="Set your user token in `~/.egggist_conf",
    )
    parser.add_argument(
        "--private",
        dest="private",
        action="store_true",
        help="Make the gist private",
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        help="Turns internal logging level to DEBUG.",
    )
    return parser.parse_args() if args is None else parser.parse_args(args)


def main() -> int:
    args = cli_parser()
    logging.basicConfig(level="DEBUG" if args.debug else "ERROR")

    if not args.filename:
        print(NOTHING_TO_DO)
        return 0

    client = EggGist(check_config=False)

    client.config.username = args.name if args.name else client.config.username
    client.config.usertoken = args.token if args.token else client.config.usertoken

    client.check_config()

    client.save_config()

    for filename in args.filename:
        client.add_file(filename)

    result = client.post_gist(not args.private)

    if result is not None:
        print(f"{SUCCESS} {result.html_url}")
    else:
        print(f"{FAILURE}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
