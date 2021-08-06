"""
Small tool to push a file or clibboard contents to user's gist

Author: Preocts
Discord: Preocts#8196
Repo: https://github.com/preocts/egggist
"""
from __future__ import annotations

import json
import logging
import pathlib
from dataclasses import dataclass
from http.client import HTTPSConnection
from typing import Dict
from typing import Optional

from egggist.models.basegist import BaseGist


class EggGist:

    CONFIG_FILE = f"{pathlib.Path.home()}/.egggist_conf"

    log = logging.getLogger(__name__)

    def __init__(self) -> None:
        """Create instance and load config file"""
        self.config: ConfigFile = self._load_config()
        self.conn = HTTPSConnection(host="api.github.com", port=443, timeout=5.0)

    def _load_config(self) -> ConfigFile:
        """Loads JSON config from user home directory"""
        if not pathlib.Path(self.CONFIG_FILE).exists():
            return ConfigFile()

        with open(self.CONFIG_FILE, "r", encoding="utf-8") as infile:
            return ConfigFile.from_dict(json.load(infile))

    def _build_headers(self) -> Dict[str, str]:
        """Builds the header with auth key, prompts if key is not in config"""
        if self.config.username is None:
            self.config.username = input("Enter GitHub username: ")
        if self.config.usertoken is None:
            self.config.usertoken = input("Enter GitHub auth token: ")
        return {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.config.usertoken}",
            "User-Agent": self.config.username,
        }

    def post_gist(self, filename: str, filecontent: str) -> Optional[BaseGist]:
        """create a gist"""
        body = json.dumps(
            {
                "description": "Eggcellent Gist",
                "public": True,
                "files": {
                    filename: {
                        "content": filecontent,
                    },
                },
            },
        )
        self.conn.request("POST", "/gists", body=body, headers=self._build_headers())
        response = self.conn.getresponse()
        if response.status != 201:
            self.log.error("Error status: %s", response.status)
        return json.loads(response.read().decode("utf-8"))


@dataclass
class ConfigFile:
    username: Optional[str] = None
    usertoken: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> ConfigFile:
        """Create instance from dict"""
        return cls(
            username=data.get("username"),
            usertoken=data.get("usertoken"),
        )

    def as_dict(self) -> Dict[str, Optional[str]]:
        return {"username": self.username, "usertoken": self.usertoken}
