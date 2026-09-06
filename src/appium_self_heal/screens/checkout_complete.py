"""Checkout Complete screen object for Sauce Labs My Demo App."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from appium_self_heal.screens.base import BaseScreen


class CheckoutCompleteScreen(BaseScreen):
    """Encapsulates UI interactions and observable state on the Checkout Complete screen."""

    _TITLE_LOCATOR = (AppiumBy.ID, "completeTV")
    _THANK_YOU_LOCATOR = (AppiumBy.ID, "thankYouTV")

    def wait_until_loaded(self) -> CheckoutCompleteScreen:
        """Wait until the checkout complete screen is fully loaded and ready."""
        self.wait_visible(self._TITLE_LOCATOR)
        return self

    @property
    def title(self) -> str:
        """Return the checkout complete header title text."""
        return self.wait_visible(self._TITLE_LOCATOR).text

    @property
    def message(self) -> str:
        """Return the thank you confirmation message text."""
        return self.wait_visible(self._THANK_YOU_LOCATOR).text
