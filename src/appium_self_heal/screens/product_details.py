"""Product Details screen object for Sauce Labs My Demo App."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from appium_self_heal.screens.base import BaseScreen


class ProductDetailsScreen(BaseScreen):
    """Encapsulates UI interactions and observable state on the Product Details screen."""

    # Unique accessibility ID on the product details screen (color options container)
    _COLOR_PICKER = (
        AppiumBy.ACCESSIBILITY_ID,
        "Displays available colors of selected product",
    )
    _TITLE_LOCATOR = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/productTV")
    _PRICE_LOCATOR = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/priceTV")

    def wait_until_loaded(self) -> ProductDetailsScreen:
        """Wait until the product details screen is fully loaded and ready.

        Uses a unique accessibility ID present only on the product details screen,
        preventing race conditions from preceding catalog screens.
        """
        self.wait_visible(self._COLOR_PICKER)
        return self

    @property
    def name(self) -> str:
        """Return the product name displayed on the details screen."""
        return self.wait_visible(self._TITLE_LOCATOR).text

    @property
    def price(self) -> str:
        """Return the price string displayed on the details screen."""
        return self.wait_visible(self._PRICE_LOCATOR).text
