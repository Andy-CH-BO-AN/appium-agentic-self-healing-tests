"""Checkout Payment screen object for Sauce Labs My Demo App."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from appium_self_heal.screens.base import BaseScreen
from appium_self_heal.screens.checkout_review import CheckoutReviewScreen


class CheckoutPaymentScreen(BaseScreen):
    """Encapsulates UI interactions and observable state on the Checkout Payment screen."""

    _SUBTITLE_LOCATOR = (AppiumBy.ID, "enterPaymentMethodTV")
    _NAME_INPUT = (AppiumBy.ID, "nameET")
    _CARD_NUMBER_INPUT = (AppiumBy.ID, "cardNumberET")
    _EXPIRATION_DATE_INPUT = (AppiumBy.ID, "expirationDateET")
    _SECURITY_CODE_INPUT = (AppiumBy.ID, "securityCodeET")
    _REVIEW_ORDER_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Saves payment info and launches screen to review checkout data",
    )

    def wait_until_loaded(self) -> CheckoutPaymentScreen:
        """Wait until the checkout payment screen is fully loaded and ready."""
        self.wait_visible(self._SUBTITLE_LOCATOR)
        return self

    def continue_to_review(
        self,
        card_holder_name: str,
        card_number: str,
        expiration_date: str,
        security_code: str,
    ) -> CheckoutReviewScreen:
        """Enter payment details and proceed to the review order screen."""
        self.wait_visible(self._NAME_INPUT).send_keys(card_holder_name)
        self.wait_visible(self._CARD_NUMBER_INPUT).send_keys(card_number)
        self.wait_visible(self._EXPIRATION_DATE_INPUT).send_keys(expiration_date)
        self.wait_visible(self._SECURITY_CODE_INPUT).send_keys(security_code)

        review_btn = self.wait_clickable(self._REVIEW_ORDER_BUTTON)
        review_btn.click()
        return CheckoutReviewScreen(self.driver).wait_until_loaded()
