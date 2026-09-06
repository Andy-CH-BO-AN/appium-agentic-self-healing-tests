"""Login screen object for Sauce Labs My Demo App."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from appium_self_heal.screens.base import BaseScreen
from appium_self_heal.screens.checkout_address import CheckoutAddressScreen


class LoginScreen(BaseScreen):
    """Encapsulates UI interactions and observable state on the Login screen."""

    _TITLE_LOCATOR = (AppiumBy.ID, "loginTV")
    _USERNAME_INPUT = (AppiumBy.ID, "nameET")
    _PASSWORD_INPUT = (AppiumBy.ID, "passwordET")
    _LOGIN_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Tap to login with given credentials",
    )

    def wait_until_loaded(self) -> LoginScreen:
        """Wait until the login screen is fully loaded and ready."""
        self.wait_visible(self._TITLE_LOCATOR)
        return self

    def login(self, username: str, password: str) -> CheckoutAddressScreen:
        """Perform login and navigate to the checkout address screen."""
        self.wait_visible(self._USERNAME_INPUT).send_keys(username)
        self.wait_visible(self._PASSWORD_INPUT).send_keys(password)

        login_btn = self.wait_clickable(self._LOGIN_BUTTON)
        login_btn.click()
        return CheckoutAddressScreen(self.driver).wait_until_loaded()
