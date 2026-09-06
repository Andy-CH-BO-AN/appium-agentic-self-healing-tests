"""Products catalog screen object for Sauce Labs My Demo App."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from appium_self_heal.screens.base import BaseScreen
from appium_self_heal.screens.product_details import ProductDetailsScreen


class ProductsScreen(BaseScreen):
    """Encapsulates UI interactions and observable state on the Products catalog screen."""

    _TITLE_LOCATOR = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/productTV")

    @property
    def title(self) -> str:
        """Return the header title text of the products screen.

        Explicitly waits for visibility, acting as the readiness check for this screen.
        """
        return self.wait_visible(self._TITLE_LOCATOR).text

    def product_price(self, product_name: str) -> str:
        """Return the catalog price for a given product name."""
        selector = (
            f'new UiSelector().text("{product_name}")'
            '.fromParent(new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/priceTV"))'
        )
        return self.wait_visible((AppiumBy.ANDROID_UIAUTOMATOR, selector)).text

    def open_product(self, product_name: str) -> ProductDetailsScreen:
        """Navigate to the product details screen by tapping the product's image card."""
        selector = (
            f'new UiSelector().text("{product_name}")'
            ".fromParent("
            'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/productIV")'
            ")"
        )
        product_card = self.wait_clickable((AppiumBy.ANDROID_UIAUTOMATOR, selector))
        product_card.click()
        return ProductDetailsScreen(self.driver)
