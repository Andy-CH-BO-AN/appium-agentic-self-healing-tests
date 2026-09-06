"""Screen Objects package for Sauce Labs My Demo App."""

from appium_self_heal.screens.base import BaseScreen
from appium_self_heal.screens.cart import CartScreen
from appium_self_heal.screens.checkout_address import CheckoutAddressScreen
from appium_self_heal.screens.checkout_complete import CheckoutCompleteScreen
from appium_self_heal.screens.checkout_payment import CheckoutPaymentScreen
from appium_self_heal.screens.checkout_review import CheckoutReviewScreen
from appium_self_heal.screens.login import LoginScreen
from appium_self_heal.screens.product_details import ProductDetailsScreen
from appium_self_heal.screens.products import ProductsScreen

__all__ = [
    "BaseScreen",
    "CartScreen",
    "CheckoutAddressScreen",
    "CheckoutCompleteScreen",
    "CheckoutPaymentScreen",
    "CheckoutReviewScreen",
    "LoginScreen",
    "ProductDetailsScreen",
    "ProductsScreen",
]
