"""Smoke test verifying Appium UiAutomator2 session creation and app launch."""

from __future__ import annotations

from typing import TYPE_CHECKING

from appium_self_heal.screens import ProductsScreen

if TYPE_CHECKING:
    from appium.webdriver import Remote


def test_app_launch_displays_products_screen(appium_driver: Remote) -> None:
    """Verify that Sauce Labs My Demo App launches on the emulator to the Products screen."""
    products_screen = ProductsScreen(appium_driver)

    assert products_screen.title == "Products"
