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
from typing import Dict
from typing import Optional


class EggGist:

    CONFIG_FILE = f"{pathlib.Path.home()}/.egggist_conf"

    log = logging.getLogger(__name__)

    def __init__(self) -> None:
        """Create instance and load config file"""
        self.config: ConfigFile = self._load_config()

    def _load_config(self) -> ConfigFile:
        """Loads JSON config from user home directory"""
        if not pathlib.Path(self.CONFIG_FILE).exists():
            return ConfigFile()

        with open(self.CONFIG_FILE, "r", encoding="utf-8") as infile:
            return ConfigFile.from_dict(json.load(infile))


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
