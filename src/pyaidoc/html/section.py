"""HTML Section container rendering with polymorphic cards objects in Pure OOP."""

import html
from pyaidoc.html.card import Card
from pyaidoc.html.ternary import Ternary
from pyaidoc.tool import Tools


class EmptySectionCards:
    """Renders empty state message when no tools are present."""

    def __init__(self, message: str = "Keine AI-Tools registriert.") -> None:
        self._message = message

    def html(self) -> str:
        return f'<div class="pyaidoc-empty-state">{html.escape(self._message)}</div>'

    def __str__(self) -> str:
        return self.html()


class PopulatedSectionCards:
    """Renders joined cards of registered AI tools."""

    def __init__(self, tools: Tools) -> None:
        self._tools = tools

    def html(self) -> str:
        return "".join(str(Card(tool)) for tool in self._tools)

    def __str__(self) -> str:
        return self.html()


class Section:
    """Renders the HTML section container of tool cards in Pure OOP."""

    def __init__(
        self,
        tools: Tools,
        title: str,
        empty_cards: EmptySectionCards = EmptySectionCards(),
    ) -> None:
        self._tools = tools
        self._title = title
        self._empty_cards = empty_cards

    def html(self) -> str:
        cards_content = Ternary(
            self._tools.empty(),
            self._empty_cards,
            PopulatedSectionCards(self._tools),
        )
        escaped_title = html.escape(self._title)
        return (
            '<div class="pyaidoc-container">'
            '<header class="pyaidoc-header">'
            f"<h1>{escaped_title}</h1>"
            '<p class="pyaidoc-subtitle">Dynamisch generierte Referenz aller verfügbaren Werkzeuge.</p>'
            "</header>"
            f'<div class="pyaidoc-cards">{cards_content}</div>'
            "</div>"
        )

    def __str__(self) -> str:
        return self.html()
