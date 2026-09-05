"""Smoke test verifying Appium UiAutomator2 session creation and app launch."""

from __future__ import annotations

from appium.webdriver import Remote
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from appium_self_heal.config import config


def test_app_launch_displays_products_screen(appium_driver: Remote) -> None:
    """Verify that Sauce Labs My Demo App launches on the emulator to the Products screen.

    Validates the end-to-end runtime chain: Appium session -> UiAutomator2 ->
    Android emulator -> APK launch -> UI state synchronization.
    """
    products_title_locator = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/productTV")

    title_element = WebDriverWait(appium_driver, config.explicit_wait_timeout).until(
        EC.visibility_of_element_located(products_title_locator)
    )

    assert title_element.text == "Products"
