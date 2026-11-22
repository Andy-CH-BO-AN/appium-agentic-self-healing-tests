"""Base Screen Object providing minimal explicit wait primitives."""

from __future__ import annotations

from collections.abc import Callable

from appium.webdriver import Remote
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from appium_self_heal.config import config


class LocatorTimeoutError(TimeoutException):
    """Raised when an explicit wait for a screen locator times out.

    Subclasses Selenium's ``TimeoutException`` so existing handling keeps working, while
    carrying structured context (screen, locator, wait condition) for failure diagnostics.
    """

    def __init__(
        self,
        *,
        screen: str,
        locator: tuple[str, str],
        locator_name: str | None,
        condition: str,
        timeout: float,
    ) -> None:
        name = f"{screen}.{locator_name}" if locator_name else f"{screen} (dynamic locator)"
        super().__init__(
            f"Timed out after {timeout}s waiting for {condition} of {name}: "
            f"strategy={locator[0]!r} value={locator[1]!r}"
        )
        # Selenium's WebDriverException reserves ``screen`` for a screenshot payload.
        self.screen_name = screen
        self.locator = locator
        self.locator_name = locator_name
        self.condition = condition
        self.timeout = timeout

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable representation of the locator context."""
        return {
            "screen": self.screen_name,
            "locator_name": self.locator_name,
            "strategy": self.locator[0],
            "value": self.locator[1],
            "condition": self.condition,
            "timeout_seconds": self.timeout,
        }


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
        return self._wait(locator, EC.visibility_of_element_located, "visibility", timeout)

    def wait_clickable(
        self,
        locator: tuple[str, str],
        timeout: float | None = None,
    ) -> WebElement:
        """Explicitly wait until an element located by locator becomes clickable."""
        return self._wait(locator, EC.element_to_be_clickable, "clickability", timeout)

    def _wait(
        self,
        locator: tuple[str, str],
        condition_factory: Callable[[tuple[str, str]], Callable[[Remote], WebElement]],
        condition: str,
        timeout: float | None,
    ) -> WebElement:
        effective_timeout = config.explicit_wait_timeout if timeout is None else timeout
        try:
            return WebDriverWait(self.driver, effective_timeout).until(condition_factory(locator))
        except TimeoutException as exc:
            raise LocatorTimeoutError(
                screen=type(self).__name__,
                locator=locator,
                locator_name=self._locator_name(locator),
                condition=condition,
                timeout=effective_timeout,
            ) from exc

    @classmethod
    def _locator_name(cls, locator: tuple[str, str]) -> str | None:
        """Return the class attribute name declaring this locator, or None if built dynamically."""
        for klass in cls.__mro__:
            for name, value in vars(klass).items():
                if name.startswith("_") and not name.startswith("__") and value == locator:
                    return name
        return None
