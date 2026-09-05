"""Pytest fixtures for managing Appium driver lifecycle."""

from __future__ import annotations

from pathlib import Path
from typing import Generator

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from appium_self_heal.config import config


@pytest.fixture(scope="function")
def appium_driver() -> Generator[webdriver.Remote, None, None]:
    """Provide a function-scoped Appium WebDriver session connected to an Android emulator.

    Assumes the Android emulator and Appium server are already started and ready
    in the execution environment. Pytest does not manage emulator or server lifecycles.
    """
    app_path = Path(config.app_path)
    if not app_path.is_absolute():
        repo_root = Path(__file__).resolve().parent.parent
        app_path = repo_root / app_path

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = config.device_name
    options.platform_version = config.platform_version
    options.app = str(app_path.resolve())
    options.app_package = "com.saucelabs.mydemoapp.android"
    options.app_activity = "com.saucelabs.mydemoapp.android.view.activities.SplashActivity"
    options.app_wait_activity = (
        "com.saucelabs.mydemoapp.android.view.activities.MainActivity,"
        "com.saucelabs.mydemoapp.android.view.activities.SplashActivity"
    )

    driver = webdriver.Remote(
        command_executor=config.appium_server_url,
        options=options,
    )

    try:
        yield driver
    finally:
        driver.quit()
