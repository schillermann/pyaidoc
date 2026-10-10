"""HTML documentation page renderer in Pure OOP."""

from pyaidoc.html.document import Document
from pyaidoc.html.section import Section
from pyaidoc.html.style import Style
from pyaidoc.tool import Tools


class Page:
    """Renders a Tools collection into a standalone HTML documentation page."""

    def __init__(
        self,
        tools: Tools,
        title: str = "AI Agent Tools & Function Calls",
        style: Style = Style(),
    ) -> None:
        self._tools = tools
        self._title = title
        self._style = style

    def title(self) -> str:
        return self._title

    def html(self) -> str:
        return str(
            Document(
                self._title,
                str(Section(self._tools, self._title)),
                self._style,
            )
        )

    def __str__(self) -> str:
        return self.html()
