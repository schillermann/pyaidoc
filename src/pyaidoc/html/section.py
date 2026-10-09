import html
from pyaidoc.html.card import Card
from pyaidoc.tools import Tools


class Section:
    """Renders the HTML section container of tool cards."""

    def __init__(self, tools: Tools, title: str) -> None:
        self._tools = tools
        self._title = title

    def html(self) -> str:
        if self._tools.empty():
            cards_html = '<div class="pyaidoc-empty-state">Keine AI-Tools registriert.</div>'
        else:
            cards_html = "".join(str(Card(tool)) for tool in self._tools)

        escaped_title = html.escape(self._title)
        return (
            '<div class="pyaidoc-container">'
            '<header class="pyaidoc-header">'
            f"<h1>{escaped_title}</h1>"
            '<p class="pyaidoc-subtitle">Dynamisch generierte Referenz aller verfügbaren Werkzeuge.</p>'
            "</header>"
            f'<div class="pyaidoc-cards">{cards_html}</div>'
            "</div>"
        )

    def __str__(self) -> str:
        return self.html()
