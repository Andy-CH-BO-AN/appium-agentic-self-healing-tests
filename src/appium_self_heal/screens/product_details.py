"""Product Details screen object for Sauce Labs My Demo App."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from appium_self_heal.screens.base import BaseScreen
from appium_self_heal.screens.cart import CartScreen


class ProductDetailsScreen(BaseScreen):
    """Encapsulates UI interactions and observable state on the Product Details screen."""

    # Unique accessibility ID on the product details screen (color options container)
    _COLOR_PICKER = (
        AppiumBy.ACCESSIBILITY_ID,
        "Displays available colors of selected product",
    )
    _TITLE_LOCATOR = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/productTV")
    _PRICE_LOCATOR = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/priceTV")
    _ADD_TO_CART_SCROLL = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true))'
        '.scrollIntoView(new UiSelector().description("Tap to add product to cart"))',
    )
    _ADD_TO_CART_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Tap to add product to cart")
    _CART_BADGE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartTV")
    _CART_ICON = (AppiumBy.ACCESSIBILITY_ID, "View cart")

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

    def add_to_cart(self) -> None:
        """Add current product to cart and wait for the cart badge state update."""
        self.wait_visible(self._ADD_TO_CART_SCROLL)
        add_btn = self.wait_clickable(self._ADD_TO_CART_BUTTON)
        add_btn.click()
        self.wait_visible(self._CART_BADGE)

    def open_cart(self) -> CartScreen:
        """Navigate to the cart screen by tapping the header cart icon."""
        cart_icon = self.wait_clickable(self._CART_ICON)
        cart_icon.click()
        return CartScreen(self.driver).wait_until_loaded()
