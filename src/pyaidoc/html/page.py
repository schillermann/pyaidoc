from pyaidoc.html.document import Document
from pyaidoc.html.section import Section
from pyaidoc.tools import Tools


class Page:
    """Renders a Tools collection into a standalone HTML documentation page."""

    def __init__(
        self,
        tools: Tools,
        title: str = "AI Agent Tools & Function Calls",
    ) -> None:
        self._tools = tools
        self._title = title

    def title(self) -> str:
        return self._title

    def section_html(self) -> str:
        return str(Section(self._tools, self.title()))

    def html(self) -> str:
        return str(Document(self.title(), self.section_html()))

    def __str__(self) -> str:
        return self.html()
