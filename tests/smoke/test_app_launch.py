"""Smoke test verifying Appium UiAutomator2 session creation and app launch."""

from __future__ import annotations

from appium.webdriver import Remote

from appium_self_heal.screens.products import ProductsScreen


def test_app_launch_displays_products_screen(appium_driver: Remote) -> None:
    """Verify that Sauce Labs My Demo App launches on the emulator to the Products screen."""
    products_screen = ProductsScreen(appium_driver)

    assert products_screen.title == "Products"
