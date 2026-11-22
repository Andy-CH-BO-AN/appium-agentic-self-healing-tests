"""Pure helpers that turn a test failure into structured, redacted diagnostics.

These functions have no Appium session dependency. The pytest hook in tests/conftest.py
is responsible for collecting the raw inputs.
"""

from __future__ import annotations

import traceback
import xml.etree.ElementTree as ET
from collections.abc import Iterable

from appium_self_heal.screens.base import LocatorTimeoutError

REDACTED = "[REDACTED]"

FAILURE_KIND_LOCATOR_TIMEOUT = "locator_timeout"
FAILURE_KIND_ASSERTION = "assertion"
FAILURE_KIND_OTHER = "other"


def classify_failure(exc: BaseException) -> str:
    """Classify a failure so downstream tooling only attempts healing on locator timeouts."""
    if isinstance(exc, LocatorTimeoutError):
        return FAILURE_KIND_LOCATOR_TIMEOUT
    if isinstance(exc, AssertionError):
        return FAILURE_KIND_ASSERTION
    return FAILURE_KIND_OTHER


def build_failure_context(
    *,
    nodeid: str,
    phase: str,
    exc: BaseException | None,
    current_package: str | None = None,
    current_activity: str | None = None,
    sensitive_values: Iterable[str] = (),
) -> dict[str, object]:
    """Build the JSON-serializable content of failure.json."""
    secrets = tuple(sensitive_values)
    data: dict[str, object] = {
        "nodeid": nodeid,
        "test_name": nodeid.split("::")[-1],
        "phase": phase,
        "app_state": {
            "current_package": current_package,
            "current_activity": current_activity,
        },
    }
    if exc is None:
        return data

    data["failure_kind"] = classify_failure(exc)
    data["exception"] = {
        "type": f"{type(exc).__module__}.{type(exc).__qualname__}",
        "message": redact_text(str(exc), secrets),
        "traceback": redact_text("".join(traceback.format_exception(exc)), secrets),
    }
    if isinstance(exc, LocatorTimeoutError):
        data["locator"] = exc.to_dict()
    return data


def redact_text(text: str, sensitive_values: Iterable[str]) -> str:
    """Replace every occurrence of each sensitive value in text."""
    for value in sensitive_values:
        if value:
            text = text.replace(value, REDACTED)
    return text


def redact_page_source(page_source: str, sensitive_values: Iterable[str]) -> str:
    """Return the Android page source with secrets and password field contents removed.

    - Any attribute containing a configured sensitive value has that value replaced.
    - The ``text`` attribute of nodes flagged ``password="true"`` is replaced entirely.

    Raises ``xml.etree.ElementTree.ParseError`` for unparseable input so callers can
    decide not to persist unredacted content.
    """
    secrets = tuple(sensitive_values)
    root = ET.fromstring(page_source)
    for node in root.iter():
        for name, value in list(node.attrib.items()):
            node.attrib[name] = redact_text(value, secrets)
        if node.attrib.get("password") == "true" and node.attrib.get("text"):
            node.attrib["text"] = REDACTED
    return ET.tostring(root, encoding="unicode", xml_declaration=True)
