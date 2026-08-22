"""Application configuration.

Loads environment variables from a local ".env" file (if present) and exposes
them as a single Settings object. Keeping all configuration in one place makes
it easy to see what the app depends on without hunting through the codebase.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load variables from .env so local development does not need real secrets.
load_dotenv()

# Project root is the parent of the "app" package directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings:
    """Simple container for app-wide settings.

    Reading values here (rather than calling os.getenv across the codebase)
    gives every module a single, typed source of truth for configuration.
    """

    # SQLite path for development. Defaults to a file next to the project root.
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./synq.db")

    # AI provider credentials. Empty string means "not configured".
    # The rest of the app never reads these names; only ai_service does.
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    # Public origin used to build team invite links.
    app_base_url: str = os.getenv("APP_BASE_URL", "http://localhost:8080").rstrip("/")

    # Signs NiceGUI browser storage (the current user id). Not an AI secret.
    storage_secret: str = os.getenv("STORAGE_SECRET", "synq-local-dev-storage")

    # Placeholder for future OAuth integrations.
    github_client_id: str = os.getenv("GITHUB_CLIENT_ID", "")
    github_client_secret: str = os.getenv("GITHUB_CLIENT_SECRET", "")


# Single shared instance imported by other modules.
settings = Settings()
