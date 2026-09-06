"""End-to-end test verifying product addition to cart and data consistency."""

from __future__ import annotations

from appium.webdriver import Remote

from appium_self_heal.screens.products import ProductsScreen


def test_add_product_to_cart(appium_driver: Remote) -> None:
    """Verify adding a product to the cart preserves catalog details and quantity.

    Navigates from catalog to product details, adds the item to the cart,
    and asserts that product name, expected price, and unit quantity match in cart.
    """
    target_product = "Sauce Labs Backpack"

    products_screen = ProductsScreen(appium_driver)
    expected_price = products_screen.product_price(target_product)

    details_screen = products_screen.open_product(target_product)
    details_screen.add_to_cart()

    cart_screen = details_screen.open_cart()

    assert cart_screen.has_product(target_product)
    assert cart_screen.product_price(target_product) == expected_price
    assert cart_screen.quantity == 1
