"""Pytest fixtures and hooks for managing Appium driver lifecycle and failure diagnostics."""

from __future__ import annotations

import hashlib
import json
import logging
import re
from pathlib import Path
from typing import Generator

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from appium_self_heal.config import config
from appium_self_heal.diagnostics import build_failure_context, redact_page_source

logger = logging.getLogger(__name__)


def _to_safe_test_id(nodeid: str) -> str:
    """Convert pytest nodeid into a deterministic, filesystem-safe, and unique directory name."""
    safe_name = re.sub(r"[^\w\-.]", "_", nodeid)
    safe_name = re.sub(r"_+", "_", safe_name).strip("_")
    digest = hashlib.sha256(nodeid.encode("utf-8")).hexdigest()[:10]
    return f"{safe_name}-{digest}"


def _safe_driver_attr(driver: webdriver.Remote, name: str) -> str | None:
    """Read a driver property for diagnostics without letting its failure propagate."""
    try:
        return getattr(driver, name)
    except Exception:
        return None


def _capture_failure_diagnostics(
    driver: webdriver.Remote,
    nodeid: str,
    phase: str = "call",
    exc: BaseException | None = None,
) -> None:
    """Capture screenshot, redacted page source, and structured failure context.

    Guarantees that diagnostic errors never mask or replace the original test failure.
    """
    try:
        test_id = _to_safe_test_id(nodeid)
        results_dir = Path("test-results") / test_id
        results_dir.mkdir(parents=True, exist_ok=True)
        sensitive_values = config.sensitive_values

        screenshot_path = results_dir / "screenshot.png"
        driver.save_screenshot(str(screenshot_path))

        failure_data = build_failure_context(
            nodeid=nodeid,
            phase=phase,
            exc=exc,
            current_package=_safe_driver_attr(driver, "current_package"),
            current_activity=_safe_driver_attr(driver, "current_activity"),
            sensitive_values=sensitive_values,
        )
        failure_path = results_dir / "failure.json"
        failure_path.write_text(json.dumps(failure_data, indent=2), encoding="utf-8")

        # Never persist page source that could not be redacted.
        page_source_path = results_dir / "page-source.xml"
        page_source_path.write_text(
            redact_page_source(driver.page_source, sensitive_values),
            encoding="utf-8",
        )
    except Exception as diag_exc:
        logger.warning(
            "Failed to capture test failure diagnostics for %s: %s",
            nodeid,
            diag_exc,
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
            exc = call.excinfo.value if call.excinfo is not None else None
            _capture_failure_diagnostics(driver, item.nodeid, phase=report.when, exc=exc)


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


@pytest.fixture(scope="function")
def test_credentials() -> tuple[str, str]:
    """Provide validated test username and password from configuration.

    Validates credentials before starting the E2E user journey; fails fast
    with ValueError if unset.
    """
    return config.test_username, config.test_password
