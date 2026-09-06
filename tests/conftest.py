"""Pytest fixtures and hooks for managing Appium driver lifecycle and failure diagnostics."""

from __future__ import annotations

import hashlib
import logging
import re
from pathlib import Path
from typing import Generator

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from appium_self_heal.config import config

logger = logging.getLogger(__name__)


def _to_safe_test_id(nodeid: str) -> str:
    """Convert pytest nodeid into a deterministic, filesystem-safe, and unique directory name."""
    safe_name = re.sub(r"[^\w\-.]", "_", nodeid)
    safe_name = re.sub(r"_+", "_", safe_name).strip("_")
    digest = hashlib.sha256(nodeid.encode("utf-8")).hexdigest()[:10]
    return f"{safe_name}-{digest}"


def _capture_failure_diagnostics(driver: webdriver.Remote, nodeid: str) -> None:
    """Capture screenshot and page source for a failed test.

    Guarantees that diagnostic errors never mask or replace the original test failure.
    """
    try:
        test_id = _to_safe_test_id(nodeid)
        results_dir = Path("test-results") / test_id
        results_dir.mkdir(parents=True, exist_ok=True)

        screenshot_path = results_dir / "screenshot.png"
        driver.save_screenshot(str(screenshot_path))

        page_source_path = results_dir / "page-source.xml"
        page_source_path.write_text(driver.page_source, encoding="utf-8")
    except Exception as exc:
        logger.warning(
            "Failed to capture test failure diagnostics for %s: %s",
            nodeid,
            exc,
            exc_info=True,
        )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item,
    call: pytest.CallInfo[None],
) -> Generator[None, None, None]:
    """Capture failure diagnostics immediately upon test failure while the session is alive."""
    outcome = yield
    report = outcome.get_result()

    if report.when in ("setup", "call") and report.failed:
        driver = item.funcargs.get("appium_driver") if hasattr(item, "funcargs") else None
        if driver is not None:
            _capture_failure_diagnostics(driver, item.nodeid)


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
