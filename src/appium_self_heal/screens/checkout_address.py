"""Checkout Address screen object for Sauce Labs My Demo App."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from appium_self_heal.screens.base import BaseScreen
from appium_self_heal.screens.checkout_payment import CheckoutPaymentScreen


class CheckoutAddressScreen(BaseScreen):
    """Encapsulates UI interactions and observable state on the Checkout Address screen."""

    _SUBTITLE_LOCATOR = (AppiumBy.ID, "enterShippingAddressTV")
    _FULL_NAME_INPUT = (AppiumBy.ID, "fullNameET")
    _ADDRESS1_INPUT = (AppiumBy.ID, "address1ET")
    _CITY_INPUT = (AppiumBy.ID, "cityET")
    _ZIP_INPUT = (AppiumBy.ID, "zipET")
    _COUNTRY_INPUT = (AppiumBy.ID, "countryET")
    _TO_PAYMENT_BUTTON = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true))'
        '.scrollIntoView(new UiSelector().description("Saves user info for checkout"))',
    )

    def wait_until_loaded(self) -> CheckoutAddressScreen:
        """Wait until the checkout address screen is fully loaded and ready."""
        self.wait_visible(self._SUBTITLE_LOCATOR)
        return self

    def continue_to_payment(
        self,
        full_name: str,
        address1: str,
        city: str,
        zip_code: str,
        country: str,
    ) -> CheckoutPaymentScreen:
        """Enter shipping address details and proceed to the payment screen."""
        self.wait_visible(self._FULL_NAME_INPUT).send_keys(full_name)
        self.wait_visible(self._ADDRESS1_INPUT).send_keys(address1)
        self.wait_visible(self._CITY_INPUT).send_keys(city)

        # Scroll down to reveal Zip, Country, and Payment button
        payment_btn = self.wait_clickable(self._TO_PAYMENT_BUTTON)

        self.wait_visible(self._ZIP_INPUT).send_keys(zip_code)
        self.wait_visible(self._COUNTRY_INPUT).send_keys(country)

        payment_btn.click()
        return CheckoutPaymentScreen(self.driver).wait_until_loaded()
