"""Dataclass"""
from dataclasses import dataclass


@dataclass
class BaseGist:
    """Base Gist response"""

    url: str = ""
    forks_url: str = ""
    commits_url: str = ""
    id: str = ""
    node_id: str = ""
    git_pull_url: str = ""
    git_push_url: str = ""
    html_url: str = ""
    created_at: str = ""
    updated_at: str = ""
    description: str = ""
    comments: int = 0
    comments_url: str = ""
