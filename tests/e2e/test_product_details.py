"""End-to-end test verifying product navigation and cross-screen data consistency."""

from __future__ import annotations

from appium.webdriver import Remote

from appium_self_heal.screens.products import ProductsScreen


def test_select_product_displays_consistent_details(appium_driver: Remote) -> None:
    """Verify selecting a catalog product displays matching product details.

    Ensures clean Screen Object boundaries, reliable cross-screen navigation,
    and cross-screen data consistency between catalog and details screens.
    """
    target_product = "Sauce Labs Backpack"

    products_screen = ProductsScreen(appium_driver)
    expected_price = products_screen.product_price(target_product)

    details_screen = products_screen.open_product(target_product)

    assert details_screen.name == target_product
    assert details_screen.price == expected_price
