"""Cart screen object for Sauce Labs My Demo App."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from appium_self_heal.screens.base import BaseScreen
from appium_self_heal.screens.login import LoginScreen


class CartScreen(BaseScreen):
    """Encapsulates UI interactions and observable state on the Cart screen."""

    _TITLE_LOCATOR = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/productTV")'
        '.text("My Cart")',
    )
    _CHECKOUT_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Confirms products for checkout",
    )

    def wait_until_loaded(self) -> CartScreen:
        """Wait until the cart screen is fully loaded and ready."""
        self.wait_visible(self._TITLE_LOCATOR)
        return self

    def has_product(self, product_name: str) -> bool:
        """Return True if a product with the specified name is visible in the cart."""
        selector = (
            f'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/titleTV")'
            f'.text("{product_name}")'
        )
        try:
            self.wait_visible((AppiumBy.ANDROID_UIAUTOMATOR, selector))
            return True
        except Exception:
            return False

    def product_price(self, product_name: str) -> str:
        """Return the unit price string for a product in the cart."""
        selector = (
            f'new UiSelector().text("{product_name}")'
            '.fromParent(new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/priceTV"))'
        )
        return self.wait_visible((AppiumBy.ANDROID_UIAUTOMATOR, selector)).text

    def product_quantity(self, product_name: str) -> int:
        """Return the quantity for a product in the cart."""
        return int(
            self.wait_visible((AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/noTV")).text
        )

    def checkout(self) -> LoginScreen:
        """Proceed to checkout and navigate to the login screen."""
        checkout_btn = self.wait_clickable(self._CHECKOUT_BUTTON)
        checkout_btn.click()
        return LoginScreen(self.driver).wait_until_loaded()
