"""Configuration module reading from os.environ."""

import os


def get_config() -> dict[str, str | bool]:
    """Read APP_MODE from environment; default to 'production'."""
    mode = os.environ.get("APP_MODE", "production")
    return {"APP_MODE": mode, "debug": mode == "development"}
