"""Base Screen Object providing minimal explicit wait primitives."""

from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from appium_self_heal.config import config

if TYPE_CHECKING:
    from appium.webdriver import Remote
    from selenium.webdriver.remote.webelement import WebElement


class BaseScreen:
    """Base class for all screen objects.

    Provides core synchronization primitives built strictly on WebDriverWait and
    Selenium expected conditions. Does not wrap element interactions or introduce
    speculative retry logic.
    """

    def __init__(self, driver: Remote) -> None:
        self.driver = driver

    def wait_visible(
        self,
        locator: tuple[str, str],
        timeout: float | None = None,
    ) -> WebElement:
        """Explicitly wait until an element located by locator becomes visible."""
        effective_timeout = config.explicit_wait_timeout if timeout is None else timeout
        return WebDriverWait(self.driver, effective_timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_clickable(
        self,
        locator: tuple[str, str],
        timeout: float | None = None,
    ) -> WebElement:
        """Explicitly wait until an element located by locator becomes clickable."""
        effective_timeout = config.explicit_wait_timeout if timeout is None else timeout
        return WebDriverWait(self.driver, effective_timeout).until(
            EC.element_to_be_clickable(locator)
        )
