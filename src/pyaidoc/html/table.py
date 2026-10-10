"""HTML Table rendering with polymorphic content objects in Pure OOP."""

import html
from pyaidoc.html.row import Row
from pyaidoc.html.ternary import Ternary
from pyaidoc.tool import Parameters


class EmptyTableContent:
    """Renders fallback message when parameters collection is empty."""

    def __init__(self, message: str = "Keine Parameter erforderlich.") -> None:
        self._message = message

    def html(self) -> str:
        return f'<p class="pyaidoc-no-params">{html.escape(self._message)}</p>'

    def __str__(self) -> str:
        return self.html()


class PopulatedTableContent:
    """Renders parameters table with headers and rows."""

    def __init__(self, params: Parameters) -> None:
        self._params = params

    def html(self) -> str:
        rows_html = "".join(str(Row(param)) for param in self._params)
        return (
            '<table class="pyaidoc-table">'
            "<thead><tr>"
            "<th>Parameter</th><th>Typ</th><th>Status</th><th>Standardwert</th>"
            "</tr></thead>"
            f"<tbody>{rows_html}</tbody>"
            "</table>"
        )

    def __str__(self) -> str:
        return self.html()


class Table:
    """Renders Parameters collection as an HTML table in Pure OOP."""

    def __init__(
        self,
        params: Parameters,
        empty_content: EmptyTableContent = EmptyTableContent(),
    ) -> None:
        self._params = params
        self._empty_content = empty_content

    def html(self) -> str:
        return str(
            Ternary(
                self._params.empty(),
                self._empty_content,
                PopulatedTableContent(self._params),
            )
        )

    def __str__(self) -> str:
        return self.html()
