"""HTML Card rendering in Pure OOP."""

import html
from typing import Any
from pyaidoc.html.table import Table
from pyaidoc.tool import Tool


class Card:
    """Renders a single Tool as an HTML component card in Pure OOP."""

    def __init__(self, tool: Tool, table: Any = "") -> None:
        self._tool = tool
        self._table = table

    def html(self) -> str:
        escaped_name = html.escape(self._tool.name())
        escaped_desc = html.escape(self._tool.description()).replace("\n", "<br>")
        table_html = str(self._table) if self._table else str(Table(self._tool.parameters()))

        return (
            '<div class="pyaidoc-card">'
            '<div class="pyaidoc-card-header">'
            f'<h3 class="pyaidoc-card-title">{escaped_name}</h3>'
            "</div>"
            f'<p class="pyaidoc-card-desc">{escaped_desc}</p>'
            f"{table_html}"
            "</div>"
        )

    def __str__(self) -> str:
        return self.html()
