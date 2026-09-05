"""Minimal runtime configuration for Phase 1 Appium Android emulator execution."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppiumConfig:
    """Runtime configuration values sourced from environment variables with sensible defaults."""

    appium_server_url: str = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
    platform_version: str = os.getenv("ANDROID_PLATFORM_VERSION", "14")
    device_name: str = os.getenv("ANDROID_DEVICE_NAME", "Android Emulator")
    app_path: str = os.getenv("ANDROID_APP_PATH", "apps/mda-2.2.0-238.apk")
    explicit_wait_timeout: float = float(os.getenv("EXPLICIT_WAIT_TIMEOUT_SECONDS", "10.0"))


# Default singleton instance for direct import
config = AppiumConfig()
