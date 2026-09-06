"""Checkout Review screen object for Sauce Labs My Demo App."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from appium_self_heal.screens.base import BaseScreen
from appium_self_heal.screens.checkout_complete import CheckoutCompleteScreen


class CheckoutReviewScreen(BaseScreen):
    """Encapsulates UI interactions and observable state on the Checkout Review screen."""

    _SUBTITLE_LOCATOR = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/enterShippingAddressTV")'
        '.text("Review your order")',
    )
    _PLACE_ORDER_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Completes the process of checkout",
    )

    def wait_until_loaded(self) -> CheckoutReviewScreen:
        """Wait until the checkout review screen is fully loaded and ready."""
        self.wait_visible(self._SUBTITLE_LOCATOR)
        return self

    def place_order(self) -> CheckoutCompleteScreen:
        """Place the order and navigate to the checkout complete screen."""
        place_order_btn = self.wait_clickable(self._PLACE_ORDER_BUTTON)
        place_order_btn.click()
        return CheckoutCompleteScreen(self.driver).wait_until_loaded()
