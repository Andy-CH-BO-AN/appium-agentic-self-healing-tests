"""Minimal runtime configuration for Phase 1 Appium Android emulator execution."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class AppiumConfig:
    """Runtime configuration values sourced from environment variables with sensible defaults."""

    appium_server_url: str = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
    platform_version: str = os.getenv("ANDROID_PLATFORM_VERSION", "14")
    device_name: str = os.getenv("ANDROID_DEVICE_NAME", "Android Emulator")
    app_path: str = os.getenv("ANDROID_APP_PATH", "apps/mda-2.2.0-238.apk")
    explicit_wait_timeout: float = float(os.getenv("EXPLICIT_WAIT_TIMEOUT_SECONDS", "10.0"))

    @property
    def test_username(self) -> str:
        """Return TEST_USERNAME from environment, failing fast if unset."""
        username = os.getenv("TEST_USERNAME")
        if not username:
            raise ValueError(
                "Missing required environment variable TEST_USERNAME. "
                "Please define it in .env or set it in your environment."
            )
        return username

    @property
    def test_password(self) -> str:
        """Return TEST_PASSWORD from environment, failing fast if unset."""
        password = os.getenv("TEST_PASSWORD")
        if not password:
            raise ValueError(
                "Missing required environment variable TEST_PASSWORD. "
                "Please define it in .env or set it in your environment."
            )
        return password


# Default singleton instance for direct import
config = AppiumConfig()
