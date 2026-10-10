"""Extracts parameter description from a docstring in Pure OOP."""

import re
from typing import Any, Callable
from pyaidoc.docstring import Docstring


class DocstringParam:
    """Extracts description for a specific parameter name from a callable docstring."""

    def __init__(self, origin: Callable[..., Any], name: str) -> None:
        self._origin = origin
        self._name = name

    def text(self) -> str:
        doc = Docstring(self._origin).text()
        if not doc:
            return ""

        # Sphinx / Epydoc style: :param <name>: <desc> or @param <name>: <desc>
        sphinx_match = re.search(
            rf"[:@]param\s+{re.escape(self._name)}\s*:\s*([^\n\r]+(?:\n[ \t]+[^\n\r]+)*)",
            doc,
            re.IGNORECASE,
        )
        if sphinx_match:
            return " ".join(line.strip() for line in sphinx_match.group(1).splitlines()).strip()

        # Google style:
        # Args:
        #     <name>: <desc>
        #     <name> (type): <desc>
        google_match = re.search(
            rf"(?:Args|Parameters):\s*\n(?:[ \t]+[^\n]+\n)*?[ \t]+{re.escape(self._name)}(?:\s*\([^)]+\))?\s*:\s*([^\n\r]+(?:\n[ \t]{{4,}}[^\n\r]+)*)",
            doc,
            re.IGNORECASE,
        )
        if google_match:
            return " ".join(line.strip() for line in google_match.group(1).splitlines()).strip()

        return ""

    def __str__(self) -> str:
        return self.text()
