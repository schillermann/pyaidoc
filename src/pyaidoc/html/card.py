import html
from pyaidoc.html.table import Table
from pyaidoc.tool import Tool


class Card:
    """Renders a single Tool as an HTML component card."""

    def __init__(self, tool: Tool) -> None:
        self._tool = tool

    def html(self) -> str:
        escaped_name = html.escape(self._tool.name())
        escaped_desc = html.escape(self._tool.description()).replace("\n", "<br>")
        table_html = str(Table(self._tool.parameters()))

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
