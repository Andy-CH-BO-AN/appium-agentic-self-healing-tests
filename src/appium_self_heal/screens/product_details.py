"""Product Details screen object for Sauce Labs My Demo App."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from appium_self_heal.screens.base import BaseScreen


class ProductDetailsScreen(BaseScreen):
    """Encapsulates UI interactions and observable state on the Product Details screen."""

    # Accessibility ID is priority 1 for distinguishing the product details screen
    _SELECTED_PRODUCT_IMAGE = (AppiumBy.ACCESSIBILITY_ID, "Displays selected product")
    _TITLE_LOCATOR = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/productTV")
    _PRICE_LOCATOR = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/priceTV")

    @property
    def name(self) -> str:
        """Return the product name displayed on the details screen.

        Explicitly synchronizes on the unique details screen element to prevent
        stale reads from preceding screens.
        """
        self.wait_visible(self._SELECTED_PRODUCT_IMAGE)
        return self.wait_visible(self._TITLE_LOCATOR).text

    @property
    def price(self) -> str:
        """Return the price string displayed on the details screen."""
        return self.wait_visible(self._PRICE_LOCATOR).text
