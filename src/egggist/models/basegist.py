"""
Data model for a GitHub Gist create response

Missing: dataclass for `forks`
"""
from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


@dataclass
class Files:
    filename: str
    type: str
    language: str
    raw_url: str
    size: int
    truncated: bool
    content: str


@dataclass
class User:
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    site_admin: bool


@dataclass
class ChangeStatus:
    total: int
    addititions: int
    deletions: int


@dataclass
class History:
    user: User
    version: str
    committed_at: str
    change_status: ChangeStatus
    url: str


@dataclass
class BaseGist:
    """Base Gist response"""

    url: str
    forks_url: str
    commits_url: str
    id: str
    node_id: str
    git_pull_url: str
    git_push_url: str
    html_url: str
    files: Dict[str, Files]
    public: bool
    created_at: str
    updated_at: str
    description: str
    user: Optional[str]
    comments: int
    comments_url: str
    owner: User
    forks: List[Any]
    history: List[History]
    truncated: bool

    @property
    def as_dict(self) -> Dict[str, Any]:
        """Returns dataclass as a dictionary"""
        return asdict(self)
