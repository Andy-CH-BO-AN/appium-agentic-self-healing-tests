"""Screen Objects package for Sauce Labs My Demo App."""

from appium_self_heal.screens.base import BaseScreen
from appium_self_heal.screens.product_details import ProductDetailsScreen
from appium_self_heal.screens.products import ProductsScreen

__all__ = [
    "BaseScreen",
    "ProductDetailsScreen",
    "ProductsScreen",
]
