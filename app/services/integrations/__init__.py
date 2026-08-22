"""Pluggable sources that normalize outside activity into WorkActivity rows.

To add another source later:
1. Create a module such as linear.py.
2. Implement the Integration interface from base.py.
3. Return WorkActivity objects from its fetch_activities method.
"""

from app.services.integrations.base import Integration
from app.services.integrations.github import GitHubIntegration
from app.services.integrations.gmail import GmailIntegration

__all__ = [
    "Integration",
    "GitHubIntegration",
    "GmailIntegration",
]
