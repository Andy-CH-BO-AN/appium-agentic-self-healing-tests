"""End-to-end test verifying complete checkout journey through order confirmation."""

from __future__ import annotations

from appium.webdriver import Remote

from appium_self_heal.screens.products import ProductsScreen


def test_complete_checkout(
    appium_driver: Remote,
    test_credentials: tuple[str, str],
) -> None:
    """Verify complete checkout journey from catalog to order confirmation screen.

    Simulates an end-to-end purchase: selects a catalog product, adds it to the cart,
    proceeds through authentication with test credentials, submits shipping and payment
    details, places the order, and verifies the final confirmation state.
    """
    # Validate credentials before starting E2E user journey; fails fast if unset
    username, password = test_credentials

    target_product = "Sauce Labs Backpack"

    # Deterministic test data for checkout flow
    shipping_full_name = "Rebecca Winter"
    shipping_address1 = "Mandorley 112"
    shipping_city = "Truro"
    shipping_zip_code = "89750"
    shipping_country = "United Kingdom"

    payment_card_holder = "Rebecca Winter"
    payment_card_number = "3258125675687891"
    payment_expiration = "0325"
    payment_security_code = "123"

    products_screen = ProductsScreen(appium_driver)
    details_screen = products_screen.open_product(target_product)
    details_screen.add_to_cart()

    cart_screen = details_screen.open_cart()
    login_screen = cart_screen.checkout()

    address_screen = login_screen.login(
        username,
        password,
    )
    payment_screen = address_screen.continue_to_payment(
        full_name=shipping_full_name,
        address1=shipping_address1,
        city=shipping_city,
        zip_code=shipping_zip_code,
        country=shipping_country,
    )
    review_screen = payment_screen.continue_to_review(
        card_holder_name=payment_card_holder,
        card_number=payment_card_number,
        expiration_date=payment_expiration,
        security_code=payment_security_code,
    )
    complete_screen = review_screen.place_order()

    assert complete_screen.title == "Checkout Complete"
    assert complete_screen.message == "Thank you for your order"
